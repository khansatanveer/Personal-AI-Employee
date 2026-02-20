"""
Script to update Dashboard counts to reflect actual file counts
"""

from pathlib import Path
import re
import datetime

def update_dashboard_counts():
    vault_path = Path(".")
    dashboard_path = vault_path / "Dashboard.md"

    if not dashboard_path.exists():
        print("Dashboard.md not found")
        return

    # Count files in each directory
    inbox_count = len(list((vault_path / 'Inbox').glob('*.md')))
    needs_action_count = len(list((vault_path / 'Needs_Action').glob('*.md')))
    done_count = len(list((vault_path / 'Done').glob('*.md')))
    pending_approval_count = len(list((vault_path / 'Pending_Approval').glob('*.md')))

    print(f"Actual counts - Inbox: {inbox_count}, Needs_Action: {needs_action_count}, Done: {done_count}, Pending_Approval: {pending_approval_count}")

    content = dashboard_path.read_text()

    # Update the dashboard content
    content = re.sub(r'Files in Inbox: \d+', f'Files in Inbox: {inbox_count}', content)
    content = re.sub(r'Files in Needs_Action: \d+', f'Files in Needs_Action: {needs_action_count}', content)
    content = re.sub(r'Files in Done: \d+', f'Files in Done: {done_count}', content)
    content = re.sub(r'Files in Pending Approval: \d+', f'Files in Pending Approval: {pending_approval_count}', content)

    # Update last updated time
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    content = re.sub(r'Last Updated: [\d\-:T\+]+', f'Last Updated: {current_time}', content)

    dashboard_path.write_text(content)
    print("Dashboard updated with correct counts")

if __name__ == "__main__":
    update_dashboard_counts()