import sys
import os
from src.crew import ProjectManagementCrew


def main():
    """Main execution function"""
    
    # Sample project input
    project_input = {
        "project_idea": "Create a Notion-integrated project management tool using AI agents.",
        "project_name": "AI-Notion Project Manager",
        "project_description": "An AI-driven tool that helps users plan, review, and track their projects seamlessly within Notion."
    }
    
    print("🚀 Starting Agentic Project Management Workflow...")
    print(f"📋 Project: {project_input['project_name']}")
    print("-" * 60)
    
    try:
        result = ProjectManagementCrew().crew().kickoff(inputs=project_input)
        
        print("\n" + "=" * 60)
        print("✅ Crew execution completed successfully!")
        print("=" * 60)
        print(f"\n📊 Results:\n{result}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()