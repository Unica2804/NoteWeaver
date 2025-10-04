#!/usr/bin/env python
"""
Main entry point for the AI Research Pipeline
Orchestrates the Information Gatherer Crew to research topics and organize them in Obsidian
"""

from src.crew import Information_Gatherer_Crew
import sys
import os
from datetime import datetime


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        AI-Powered Research & Knowledge Management         ║
    ║           Automatic Obsidian Vault Builder                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_research_topic():
    """Get research topic from user"""
    print("\n🔍 What would you like to research?")
    print("   (Enter your topic or question)")
    print("-" * 60)
    
    topic = input("Topic: ").strip()
    
    if not topic:
        print("❌ Error: Topic cannot be empty!")
        sys.exit(1)
    
    return topic


def confirm_execution(topic: str) -> bool:
    """Confirm with user before starting the research"""
    print("\n" + "=" * 60)
    print(f"📋 Research Topic: {topic}")
    print("=" * 60)
    print("\n🤖 The AI agents will:")
    print("   1. Research your topic thoroughly")
    print("   2. Convert findings to structured Markdown")
    print("   3. Organize the note in your Obsidian vault")
    print("   4. Add tags and create backlinks")
    print("\n⏱️  This may take a few minutes...")
    print("-" * 60)
    
    confirm = input("\n▶️  Proceed? (yes/no): ").strip().lower()
    return confirm in ['yes', 'y']


def run_research_pipeline(topic: str):
    """Execute the research pipeline"""
    try:
        print("\n" + "=" * 60)
        print("🚀 Starting Research Pipeline...")
        print("=" * 60)
        
        # Initialize the crew
        print("\n[1/4] Initializing AI agents...")
        crew_instance = Information_Gatherer_Crew()
        crew = crew_instance.crew()
        
        # Execute the crew with the topic
        print(f"\n[2/4] Research Agent investigating: '{topic}'")
        print("[3/4] Markdown Agent formatting results...")
        print("[4/4] Obsidian Agent organizing in vault...")
        print("\n" + "-" * 60)
        
        # Run the crew
        result = crew.kickoff(inputs={'topic': topic})
        
        # Print results
        print("\n" + "=" * 60)
        print("✅ Research Pipeline Completed!")
        print("=" * 60)
        print("\n📄 Results:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user.")
        sys.exit(0)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Error occurred during execution!")
        print("=" * 60)
        print(f"\n🔴 Error details: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   - Check your .env file for correct API keys")
        print("   - Ensure Obsidian vault path is configured")
        print("   - Verify MCP server is running")
        print("   - Check your internet connection")
        return False


def save_session_log(topic: str, success: bool):
    """Save session information to log file"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(log_dir, "session_log.txt")
    
    with open(log_file, "a") as f:
        status = "SUCCESS" if success else "FAILED"
        f.write(f"[{timestamp}] {status} - Topic: {topic}\n")


def main():
    """Main execution function"""
    # Print banner
    print_banner()
    
    # Get topic from user
    topic = get_research_topic()
    
    # Confirm execution
    if not confirm_execution(topic):
        print("\n❌ Operation cancelled by user.")
        sys.exit(0)
    
    # Run the pipeline
    success = run_research_pipeline(topic)
    
    # Save log
    save_session_log(topic, success)
    
    # Final message
    if success:
        print("\n✨ Your research has been added to your Obsidian vault!")
        print("🔗 Check your vault to explore the new note and connections.\n")
    else:
        print("\n⚠️  Pipeline completed with errors. Check the logs for details.\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())