import sys
import os
from src.crew import ProjectManagementCrew


def main():
    """Main execution function"""
    
    # Sample project input
    project_input = {
        "project_idea": """
        Build an e-commerce platform with the following features:
        - User authentication and authorization
        - Product catalog with search and filtering
        - Shopping cart and checkout system
        - Payment integration (Stripe)
        - Order management and tracking
        - Admin dashboard for inventory management
        - Email notifications
        - Mobile responsive design
        
        Timeline: 3 months
        Team size: 4 developers
        """,
        "project_name": "E-Commerce Platform",
        "project_owner": "Tech Team Lead",
        "start_date": "2025-10-15",
        "end_date": "2026-01-15"
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