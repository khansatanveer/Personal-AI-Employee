"""
Demo script to show Claude Code's ability to read from and write to the vault.
This simulates what Claude Code would do when processing files in the AI Employee system.
"""

import os
from pathlib import Path
import datetime

def simulate_claude_processing():
    """Simulate Claude Code reading and writing files in the vault"""
    vault_path = Path(".")

    print("=== Claude Code Vault Interaction Demo ===")
    print(f"Current directory: {os.getcwd()}")

    # Read Dashboard.md
    dashboard_path = vault_path / "Dashboard.md"
    if dashboard_path.exists():
        print(f"\n[SUCCESS] Successfully read Dashboard.md")
        dashboard_content = dashboard_path.read_text()
        print(f"Dashboard has {len(dashboard_content)} characters")

    # Read Company_Handbook.md
    handbook_path = vault_path / "Company_Handbook.md"
    if handbook_path.exists():
        print(f"\n[SUCCESS] Successfully read Company_Handbook.md")
        handbook_content = handbook_path.read_text()
        print(f"Handbook has {len(handbook_content)} characters")

    # Process any files in Needs_Action folder
    needs_action_path = vault_path / "Needs_Action"
    if needs_action_path.exists():
        action_files = list(needs_action_path.glob("*.md"))
        print(f"\nFound {len(action_files)} file(s) in Needs_Action folder")

        for file_path in action_files:
            print(f"  - Processing: {file_path.name}")
            content = file_path.read_text()
            print(f"    Content preview: {content[:100]}...")

            # Create a response/plan file in Plans folder
            plan_path = vault_path / "Plans" / f"PLAN_Response_{file_path.stem}.md"
            plan_content = f"""# Plan for {file_path.name}

## Task Analysis
Based on the file {file_path.name}, the following actions are needed:

1. Review the content carefully
2. Process the request appropriately
3. Update relevant systems
4. Log the completion

## Status
- Created: {datetime.datetime.now().isoformat()}
- Status: In Progress
- Assigned: Claude Code AI Employee

## Next Steps
This is a demonstration of Claude Code's ability to process files in the vault.
"""
            plan_path.write_text(plan_content)
            print(f"  - Created plan: {plan_path.name}")

    # Create a summary log
    log_path = vault_path / "Logs" / f"demo_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.md"
    log_content = f"""# Claude Code Interaction Log
Date: {datetime.datetime.now().isoformat()}

## Actions Performed
- Read Dashboard.md
- Read Company_Handbook.md
- Processed {len(action_files)} file(s) from Needs_Action
- Created plan files in Plans folder

## Status
- Vault read/write: SUCCESS
- File processing: COMPLETE
- Demo status: FINISHED
"""
    log_path.write_text(log_content)

    print(f"\n[SUCCESS] Created log file: {log_path.name}")
    print(f"\n=== Demo Complete ===")
    print("Claude Code has successfully demonstrated:")
    print("- Reading files from the vault")
    print("- Writing files to the vault")
    print("- Processing files in different folders")
    print("- Creating new files based on existing content")

if __name__ == "__main__":
    simulate_claude_processing()