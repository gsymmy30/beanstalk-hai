import os
import openai
from dotenv import load_dotenv
from agents.input_handler import InputHandler
from agents.story_generator import StoryGenerator
from agents.judge import JudgeSystem
from agents.qa import QAAgent
from utils.story_tracker import StoryTracker

load_dotenv()


def call_model(prompt: str, max_tokens=3000, temperature=0.7) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        print("\n No API key found")
        return '{"title": "NA", "story": "NA", "moral": "NA"}'

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]


def show_menu():
    print("\n" + "=" * 50)
    print("🌱✨ BEANSTALK AI ✨🌱".center(50))
    print("Magical Bedtime Stories for Kids 5-10".center(50))
    print("=" * 50)
    print("\n  📖  1. Create a new story")
    print("  📊  2. View story report")
    print("  🌙  3. Exit\n")


def display_scores(evaluation):
    if evaluation.get("scores"):
        overall = evaluation.get("overall", 0)

        if evaluation.get("pass", False):
            print(f"\n✅ Story Quality: {overall}/10")
        else:
            print(f"\n❌ Needs Improvement: {overall}/10")
            if evaluation.get("feedback"):
                print(f"   {evaluation['feedback']}")


def display_story(story):
    print("\n" + "=" * 50)
    print("✨ YOUR BEDTIME STORY ✨".center(50))
    print("=" * 50)
    print(f"\n📚 {story['title']}")
    print("-" * 50)
    print(f"\n{story['story']}")
    print(f"\n💫 {story['moral']}")
    print("-" * 50)


def create_story(input_handler, story_generator, judge_system, qa_agent, story_tracker):
    print("\n📖 What story shall we create tonight?")
    print(
        "💡 Try: 'a girl named Luna and her best friend Max, who happens to be a dragon' or \n   'a boy named Pete who loves to play pickleball'"
    )

    user_input = input("\n➤ Your idea: ").strip()

    if not user_input:
        return False

    try:
        print("\n✨ Creating your story...")
        processed = input_handler.process_input(user_input)

        if not processed["valid"]:
            print(f"\n💭 {processed['suggestion']}")
            return True

        story, outline = story_generator.generate_story(processed["story_elements"])
        initial_evaluation = judge_system.evaluate_story(story)

        if not initial_evaluation.get("safety_passed", True):
            print("\nOops! Let's try a different story idea!")
            print(f"   Reason: {initial_evaluation.get('reason', 'Safety concern')}")
            return True

        improvement = initial_evaluation.get("improvement", "")
        final_story = story
        final_evaluation = initial_evaluation

        if improvement and improvement.lower() not in [
            "story is excellent as is.",
            "no improvements needed.",
            "",
        ]:
            print("Improving story...")
            # print(improvement)
            refined_story = story_generator.refine_story(story, improvement)
            refined_evaluation = judge_system.evaluate_story(refined_story)

            if refined_evaluation.get("overall", 0) > initial_evaluation.get(
                "overall", 0
            ):
                final_story = refined_story
                final_evaluation = refined_evaluation

        display_story(final_story)
        display_scores(final_evaluation)

        print("\n💭 Did you enjoy this story? (Y/N)")
        user_liked = False
        while True:
            feedback = input("➤ ").strip().upper()
            if feedback in ["Y", "N"]:
                user_liked = feedback == "Y"
                break

        story_tracker.add_story(
            story=final_story,
            evaluation=final_evaluation,
            user_request=user_input,
            user_liked=user_liked,
        )

        if final_evaluation.get("pass", False):
            print("\n💬 Got questions about the story?")
            qa_questions = qa_agent.generate_question_opportunities(final_story)

            if qa_questions:
                print("Here are some things you could ask:")
                for i, q in enumerate(qa_questions[:3], 1):
                    print(f"  {i}. {q}")

                print("\n(Ask a question or press Enter to skip)")

                question = input("\n❓ ").strip()
                if question:
                    answer = qa_agent.answer_question(question, final_story)
                    print(f"\n💡 {answer}")

        input("\nPress Enter to continue...")
        return True

    except Exception:
        print("\n\nOops! Let's try again with a different idea.")
        return True


def main():
    input_handler = InputHandler(call_model)
    story_generator = StoryGenerator(call_model)
    judge_system = JudgeSystem(call_model)
    qa_agent = QAAgent(call_model)
    story_tracker = StoryTracker()

    print("\n🌟 Welcome to Beanstalk AI!")
    print("   Where bedtime stories come to life...")

    while True:
        show_menu()

        stats = story_tracker.get_stats()
        if stats["total"] > 0:
            print(f"📚 {stats['total']} stories created")

        choice = input("\n➤ Choose: ").strip()

        if choice == "1":
            create_story(
                input_handler, story_generator, judge_system, qa_agent, story_tracker
            )

        elif choice == "2":
            if stats["total"] == 0:
                print("\n->  No stories yet! Create one first.")
            else:
                story_tracker.generate_html_report()
                print("\n-> Report saved as 'story_report.html'")
                print("   Open it in your browser to see your stories!")
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\n🌙 Sweet dreams!")
            print("   Thanks for using Beanstalk AI")
            break

        else:
            print("\n Just type 1, 2, or 3")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Sweet dreams!")
    except Exception as e:
        print(f"\n Something went wrong: {e}")
        print("Please restart the app.")
