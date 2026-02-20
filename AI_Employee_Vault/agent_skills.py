"""
Agent Skills for the AI Employee System

This module contains various agent skills that Claude Code can use to interact with the vault system.
These are functions that would be registered as skills for the Claude Code agent.
"""

from pathlib import Path
import datetime
import json

class AIEmployeeSkills:
    """Collection of skills for the AI Employee"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)

    def read_dashboard_status(self) -> dict:
        """Read the current dashboard status"""
        dashboard_path = self.vault_path / "Dashboard.md"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            # Simple parsing to extract key information
            return {
                "file_exists": True,
                "content_length": len(content),
                "last_updated": self._extract_last_updated(content),
                "recent_activity_count": content.count("Recent Activity")  # Simplified
            }
        return {"file_exists": False}

    def _extract_last_updated(self, content: str) -> str:
        """Extract last updated timestamp from dashboard"""
        for line in content.split('\n'):
            if 'Last Updated:' in line:
                return line.split('Last Updated:')[1].strip()
        return "Unknown"

    def get_needs_action_files(self) -> list:
        """Get list of files in Needs_Action folder"""
        needs_action_path = self.vault_path / "Needs_Action"
        if needs_action_path.exists():
            files = list(needs_action_path.glob("*.md"))
            return [{"name": f.name, "size": f.stat().st_size, "path": str(f)} for f in files]
        return []

    def create_plan_file(self, task_description: str, related_file: str = None) -> str:
        """Create a plan file in the Plans folder"""
        plans_path = self.vault_path / "Plans"
        plans_path.mkdir(exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_filename = f"PLAN_{timestamp}_{related_file or 'general'}.md"
        plan_path = plans_path / plan_filename

        plan_content = f"""# Plan File
Created: {datetime.datetime.now().isoformat()}
Related to: {related_file or 'General task'}

## Task Description
{task_description}

## Steps to Complete
1. Analyze the requirements
2. Execute the necessary actions
3. Validate the results
4. Update the system status

## Status
- Created: {datetime.datetime.now().isoformat()}
- Status: In Progress
- Assigned: AI Employee
"""
        plan_path.write_text(plan_content)
        return str(plan_path)

    def move_file_to_done(self, file_path: str) -> bool:
        """Move a file from Needs_Action to Done folder"""
        source_path = self.vault_path / file_path
        if not source_path.exists():
            return False

        done_path = self.vault_path / "Done"
        done_path.mkdir(exist_ok=True)

        # Move the file to Done folder
        dest_path = done_path / source_path.name
        source_path.rename(dest_path)
        return True

    def update_dashboard_activity(self, activity_description: str):
        """Update the dashboard with new activity"""
        dashboard_path = self.vault_path / "Dashboard.md"
        if not dashboard_path.exists():
            return

        content = dashboard_path.read_text()

        # Find the Recent Activity section
        lines = content.split('\n')
        new_lines = []
        in_recent_activity = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith('## Recent Activity'):
                # Insert the new activity as the next line
                new_lines.append(f"- [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {activity_description}")
                in_recent_activity = True

        updated_content = '\n'.join(new_lines)

        # Update the last updated timestamp
        import re
        current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        updated_content = re.sub(r'Last Updated: [\d\-:T\+]+', f'Last Updated: {current_time}', updated_content)

        dashboard_path.write_text(updated_content)

    def get_company_handbook_rules(self) -> str:
        """Get the company handbook content"""
        handbook_path = self.vault_path / "Company_Handbook.md"
        if handbook_path.exists():
            return handbook_path.read_text()
        return "Company Handbook not found"

# Example usage
if __name__ == "__main__":
    skills = AIEmployeeSkills()

    print("=== AI Employee Skills Demo ===")

    # Test reading dashboard
    dashboard_info = skills.read_dashboard_status()
    print(f"Dashboard info: {dashboard_info}")

    # Test getting needs action files
    needs_action_files = skills.get_needs_action_files()
    print(f"Needs Action files: {needs_action_files}")

    # Test creating a plan
    plan_path = skills.create_plan_file("Process test request from client", "Test_Request.md")
    print(f"Created plan at: {plan_path}")

    # Test updating dashboard
    skills.update_dashboard_activity("Created test plan for client request")
    print("Dashboard updated with new activity")

    print("Skills demo completed successfully!")