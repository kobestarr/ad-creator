#!/bin/bash
# Asana Integration for Morning Briefing
# Pulls tasks and project status from Bluprintx Asana

ASANA_TOKEN="2/1211972939915212/1213117206506140:9ea53434303579f6f20197aeb645f908"
WORKSPACE_ID="1203345736110602"
USER_ID="1211972939915212"

echo "🎯 ASANA - BLUPRINTX TASKS"
echo "────────────────────────────────────────────"

# Get today's date in format Asana uses (YYYY-MM-DD)
TODAY=$(date +%Y-%m-%d)
THIS_WEEK=$(date -d "+7 days" +%Y-%m-%d)

# Function to get tasks due today
echo "📅 DUE TODAY:"
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces/$WORKSPACE_ID/tasks?assignee=$USER_ID&completed=false&due_on=$TODAY&opt_fields=name,projects.name,due_on" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
tasks = data.get('data', [])
if tasks:
    for task in tasks:
        name = task.get('name', 'Unnamed task')
        projects = task.get('projects', [])
        project_name = projects[0].get('name') if projects else 'No project'
        print(f'• {name} ({project_name})')
else:
    print('✅ No tasks due today!')
"

echo ""
echo "📋 OVERDUE TASKS:"
# Get overdue tasks
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces/$WORKSPACE_ID/tasks?assignee=$USER_ID&completed=false&due_before=$TODAY&opt_fields=name,projects.name,due_on" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
tasks = data.get('data', [])
if tasks:
    for task in tasks:
        name = task.get('name', 'Unnamed task')
        due_date = task.get('due_on', 'No date')
        projects = task.get('projects', [])
        project_name = projects[0].get('name') if projects else 'No project'
        print(f'⚠️ {name} ({project_name}) - Due: {due_date}')
else:
    print('✅ No overdue tasks!')
"

echo ""
echo "📈 PROJECT SUMMARY:"
# Get all active projects
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces/$WORKSPACE_ID/projects?archived=false&opt_fields=name,created_at" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
projects = data.get('data', [])
if projects:
    print(f'Active Projects: {len(projects)}')
    for project in projects[:5]:  # Show top 5
        name = project.get('name', 'Unnamed project')
        print(f'• {name}')
    if len(projects) > 5:
        print(f'... and {len(projects) - 5} more')
"

echo ""
echo "🎯 THIS WEEK'S FOCUS:"
# Get tasks due this week
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces/$WORKSPACE_ID/tasks?assignee=$USER_ID&completed=false&due_after=$TODAY&due_before=$THIS_WEEK&opt_fields=name,projects.name,due_on" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
tasks = data.get('data', [])
if tasks:
    print(f'Tasks this week: {len(tasks)}')
    # Group by due date
    by_date = {}
    for task in tasks:
        due_date = task.get('due_on', 'No date')
        name = task.get('name', 'Unnamed task')
        if due_date not in by_date:
            by_date[due_date] = []
        by_date[due_date].append(name)
    
    for date, task_names in sorted(by_date.items()):
        print(f'{date}: {len(task_names)} tasks')
else:
    print('No tasks scheduled this week')
"

echo ""
echo "📊 TASK STATS:"
# Get task statistics
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces/$WORKSPACE_ID/tasks?assignee=$USER_ID&completed=false&opt_fields=name" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
tasks = data.get('data', [])
print(f'Active tasks: {len(tasks)}')

# Get completed tasks for comparison
curl -s -H \"Authorization: Bearer $ASANA_TOKEN\" \
  \"https://app.asana.com/api/v1.0/workspaces/$WORKSPACE_ID/tasks?assignee=$USER_ID&completed=true&opt_fields=name&limit=10\" | \
  python3 -c \"
import json,sys
data = json.load(sys.stdin)
completed = len(data.get('data', []))
print(f'Recently completed: {completed}+ tasks')
\" 2>/dev/null || echo 'Completed stats: Unable to fetch'
"

echo ""
echo "🔗 QUICK ACTIONS:"
echo "• View all tasks: https://app.asana.com/0/1203345736110602/list"
echo "• My tasks: https://app.asana.com/0/1211972939915212/list"