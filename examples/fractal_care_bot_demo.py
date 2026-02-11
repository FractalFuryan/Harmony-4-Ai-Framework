"""
Fractal Care Bot - Basic Usage Example

Demonstrates Missy + Ani dual-agent reflective system.
"""

from harmony import FractalCareBot


def main():
    print("=" * 80)
    print("Fractal Care Bot - Example Usage")
    print("=" * 80)
    print()

    # Initialize bot with seed for reproducibility
    bot = FractalCareBot(seed=42)
    print("✅ Bot initialized with seed=42 (reproducible mode)\n")

    # Example 1: Emotional input
    print("Example 1: Emotional Expression")
    print("-" * 80)
    user_input = "I feel anxious about the future"
    print(f"User: {user_input}\n")
    response = bot.process(user_input)
    print(f"Bot:\n{response}\n")
    print()

    # Example 2: Technical question
    print("Example 2: Technical Question")
    print("-" * 80)
    user_input = "How does a neural network learn?"
    print(f"User: {user_input}\n")
    response = bot.process(user_input)
    print(f"Bot:\n{response}\n")
    print()

    # Example 3: Visionary/esoteric language
    print("Example 3: Visionary Language")
    print("-" * 80)
    user_input = "The fractal spiral continues to unfold"
    print(f"User: {user_input}\n")
    response = bot.process(user_input)
    print(f"Bot:\n{response}\n")
    print()

    # Example 4: Mode switching
    print("Example 4: Mode Switching - Scientific Only")
    print("-" * 80)
    print("Switching to scientific mode...\n")
    mode_response = bot.process("ani mode scientific")
    print(f"Bot: {mode_response}\n")

    user_input = "I feel overwhelmed"
    print(f"User: {user_input}\n")
    response = bot.process(user_input)
    print(f"Bot:\n{response}\n")
    print()

    # Example 5: Autonomy restoration
    print("Example 5: Autonomy Restoration")
    print("-" * 80)
    user_input = "power down"
    print(f"User: {user_input}\n")
    response = bot.process(user_input)
    print(f"Bot: {response}\n")
    print()

    # Demonstrate reproducibility
    print("=" * 80)
    print("Reproducibility Demonstration")
    print("=" * 80)
    print()

    bot1 = FractalCareBot(seed=99)
    bot2 = FractalCareBot(seed=99)

    test_input = "I'm feeling uncertain"

    response1 = bot1.process(test_input)
    response2 = bot2.process(test_input)

    print(f"Bot 1 (seed=99): First 100 chars of response:")
    print(response1[:100] + "...\n")

    print(f"Bot 2 (seed=99): First 100 chars of response:")
    print(response2[:100] + "...\n")

    if response1 == response2:
        print("✅ Responses are identical (reproducibility confirmed)")
    else:
        print("❌ Responses differ (unexpected)")

    print()
    print("=" * 80)
    print("Example complete. See docs/fractal_care_bot.md for full documentation.")
    print("=" * 80)


if __name__ == "__main__":
    main()
