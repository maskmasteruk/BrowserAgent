import asyncio
import base64
import json
import uuid
from typing import Any, Dict, List

import httpx
from playwright.async_api import async_playwright


AGENT_URL = "http://127.0.0.1:8000/agent"

START_URL = "https://facebook.com"

USER_QUERY = "Create an account."

LOCAL_SECRETS = {
    "first_name": {
        "value": "James",
        "category": "name",
        "description": "First name",
    },
    "surname": {
        "value": "Bond",
        "category": "name",
        "description": "Surname",
    },
    "date_of_birth": {
        "value": "01/01/2000",
        "category": "other",
        "description": "Date Of Birth",
    },
    "gender": {
        "value": "Male",
        "category": "other",
        "description": "Gender",
    },
    "email": {
        "value": "test@gmail.com",
        "category": "email",
        "description": "email",
    },
    "password": {
        "value": "IYVASDK:@dboidadsQ##R@",
        "category": "password",
        "description": "password",
    }
}

USER_INPUTS = {
}

MAX_AGENT_STEPS = 20


async def extract_dom(page) -> List[Dict[str, Any]]:
    return await page.evaluate(
        """
        () => {
            const elements = [];
            let counter = 0;

            const interactiveSelectors = [
                "a",
                "button",
                "input",
                "textarea",
                "select",
                "[role]",
                "[contenteditable='true']",
                "[onclick]"
            ];

            const nodes = document.querySelectorAll(
                interactiveSelectors.join(",")
            );

            for (const el of nodes) {
                const rect = el.getBoundingClientRect();

                const style = window.getComputedStyle(el);

                const visible =
                    rect.width > 0 &&
                    rect.height > 0 &&
                    style.display !== "none" &&
                    style.visibility !== "hidden" &&
                    style.opacity !== "0";

                if (!visible) {
                    continue;
                }

                let agentId = el.getAttribute("data-agent-id");

                if (!agentId) {
                    agentId = `agent-${counter++}`;
                    el.setAttribute("data-agent-id", agentId);
                }

                const tag = el.tagName.toLowerCase();

                const type = el.getAttribute("type");

                const label =
                    el.labels && el.labels.length
                        ? Array.from(el.labels)
                            .map(label => label.innerText.trim())
                            .filter(Boolean)
                            .join(" ")
                        : null;

                const ariaLabel =
                    el.getAttribute("aria-label");

                const placeholder =
                    el.getAttribute("placeholder");

                const name =
                    el.getAttribute("name");

                const role =
                    el.getAttribute("role");

                const text =
                    (el.innerText || el.textContent || "")
                        .trim()
                        .slice(0, 1000);

                const href =
                    el.getAttribute("href");

                let maskedValue = null;

                if (
                    tag === "input" ||
                    tag === "textarea" ||
                    tag === "select"
                ) {
                    const value = el.value || "";

                    if (value.length > 0) {
                        maskedValue = "[MASKED]";
                    } else {
                        maskedValue = "";
                    }
                }
                
                const item = {
                    id: agentId,
                    tag,
                    disabled: el.disabled || false,
                    visible: true
                };
                
                const optionalValues = {
                    type,
                    label,
                    aria_label: ariaLabel,
                    placeholder,
                    name,
                    role,
                    text,
                    masked_value: maskedValue,
                    href,
                    checked:
                        typeof el.checked === "boolean"
                            ? el.checked
                            : null,
                    selected:
                        typeof el.selected === "boolean"
                            ? el.selected
                            : null
                };
                
                for (const [key, value] of Object.entries(optionalValues)) {
                    if (
                        value !== null &&
                        value !== undefined &&
                        value !== ""
                    ) {
                        item[key] = value;
                    }
                }
                
                elements.push(item);
            }

            return elements;
        }
        """
    )


async def build_browser_context(page):
    elements = await extract_dom(page)

    viewport = page.viewport_size or {
        "width": 1280,
        "height": 720,
    }

    return {
        "url": page.url,
        "title": await page.title(),
        "viewport_width": viewport["width"],
        "viewport_height": viewport["height"],
        "elements": elements,
    }


async def take_screenshot_base64(page):
    screenshot_bytes = await page.screenshot(
        full_page=False
    )

    return base64.b64encode(
        screenshot_bytes
    ).decode("utf-8")


def build_available_secrets():
    return [
        {
            "key": key,
            "category": data["category"],
            "description": data.get(
                "description"
            ),
        }
        for key, data in LOCAL_SECRETS.items()
    ]


def build_user_inputs():
    return [
        {
            "key": key,
            "value": value,
        }
        for key, value in USER_INPUTS.items()
    ]


async def call_agent(
        client,
        request_id,
        query,
        browser,
        screenshot_base64=None,
):
    payload = {
        "request_id": request_id,
        "query": query,
        "browser": browser,
        "available_secrets": build_available_secrets(),
        "user_inputs": build_user_inputs(),
        "screenshot_base64": screenshot_base64,
    }

    print("\nSending request to agent...")

    try:
        response = await client.post(
            AGENT_URL,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
        return data

    except httpx.HTTPStatusError as e:
        print("\n" + "=" * 60)
        print(f"HTTP ERROR {e.response.status_code} DETAILED PAYLOAD:")
        print("=" * 60)
        try:
            print(json.dumps(e.response.json(), indent=2))
        except Exception:
            print(e.response.text)
        print("=" * 60 + "\n")
        raise e


async def get_element(page, element_id):
    locator = page.locator(
        f'[data-agent-id="{element_id}"]'
    )

    count = await locator.count()

    if count == 0:
        raise RuntimeError(
            f"Element not found: {element_id}"
        )

    return locator.first


async def execute_action(
        page,
        action,
):
    action_type = action["type"]

    print(
        f"\nExecuting: {action_type}"
    )

    if action_type == "click":
        element = await get_element(
            page,
            action["element_id"],
        )

        await element.click()

        return

    if action_type == "move":
        element = await get_element(
            page,
            action["element_id"],
        )

        await element.hover()

        return

    if action_type == "type_text":
        element = await get_element(
            page,
            action["element_id"],
        )

        await element.fill(
            action["text"]
        )

        return

    if action_type == "type_secret":
        secret_key = action["secret_key"]

        if secret_key not in LOCAL_SECRETS:
            raise RuntimeError(
                f"Local secret not found: {secret_key}"
            )

        secret_value = LOCAL_SECRETS[
            secret_key
        ]["value"]

        element = await get_element(
            page,
            action["element_id"],
        )

        await element.hover()

        await element.fill(
            secret_value
        )

        return

    if action_type == "key":
        await page.keyboard.press(
            action["key"]
        )

        return

    if action_type == "scroll":
        direction = action["direction"]

        amount = action.get(
            "amount",
            500,
        )

        x = 0
        y = 0

        if direction == "down":
            y = amount

        elif direction == "up":
            y = -amount

        elif direction == "right":
            x = amount

        elif direction == "left":
            x = -amount

        await page.mouse.wheel(
            x,
            y,
        )

        return

    if action_type == "wait":
        milliseconds = action.get(
            "milliseconds",
            1000,
        )

        await page.wait_for_timeout(
            milliseconds
        )

        return

    raise RuntimeError(
        f"Unsupported executable action: {action_type}"
    )


async def execute_actions(
        page,
        actions,
):
    for action in actions:
        action_type = action["type"]

        if action_type in {
            "request_screenshot",
            "request_user_input",
        }:
            continue

        await execute_action(
            page,
            action,
        )


async def run_browser_agent():
    request_id = str(
        uuid.uuid4()
    )

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False
        )

        context = await browser.new_context(
            viewport={
                "width": 1280,
                "height": 720,
            }
        )

        page = await context.new_page()

        await page.goto(
            START_URL,
            wait_until="domcontentloaded",
        )

        async with httpx.AsyncClient() as client:
            screenshot_base64 = None

            for step in range(
                    MAX_AGENT_STEPS
            ):
                print(
                    f"\n{'=' * 60}"
                )

                print(
                    f"Agent step: {step + 1}"
                )

                print(
                    f"{'=' * 60}"
                )

                browser_context = (
                    await build_browser_context(
                        page
                    )
                )

                agent_response = (
                    await call_agent(
                        client=client,
                        request_id=request_id,
                        query=USER_QUERY,
                        browser=browser_context,
                        screenshot_base64=screenshot_base64,
                    )
                )

                screenshot_base64 = None

                status = agent_response[
                    "status"
                ]

                actions = agent_response[
                    "actions"
                ]

                if status == "error":
                    print(
                        "\nAgent returned an error:"
                    )

                    print(
                        agent_response.get(
                            "error"
                        )
                    )

                    break

                if status == "screenshot_required":
                    print(
                        "\nAgent requested screenshot."
                    )

                    screenshot_base64 = (
                        await take_screenshot_base64(
                            page
                        )
                    )

                    continue

                if status == "user_input_required":
                    print(
                        "\nAgent requires user input:"
                    )

                    for action in actions:
                        if (
                                action["type"]
                                == "request_user_input"
                        ):
                            print(
                                json.dumps(
                                    action,
                                    indent=2,
                                )
                            )

                    break

                if status == "actions_ready":
                    await execute_actions(
                        page,
                        actions,
                    )

                    await page.wait_for_timeout(
                        500
                    )

                    if step == (
                            MAX_AGENT_STEPS - 1
                    ):
                        print(
                            "\nMaximum steps reached."
                        )

            print(
                "\nBrowser remains open for inspection."
            )

            input(
                "Press ENTER to close..."
            )

        await browser.close()


if __name__ == "__main__":
    asyncio.run(
        run_browser_agent()
    )