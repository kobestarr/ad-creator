#!/usr/bin/env python3
"""
Asana Task Optimization System
Automated task management with smart filtering and capacity planning
"""

import datetime
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class Project(Enum):
    AGENTFORCE = "Agentforce"
    REDDIT = "Reddit"
    WEBSITE = "Website"

@dataclass
class Task:
    id: str
    title: str
    project: Project
    due_date: datetime.date
    estimated_hours: float
    priority: Priority
    energy_required: int  # 1-5 scale
    dependencies: List[str]
    created_date: datetime.date

class AsanaOptimizer:
    def __init__(self):
        self.sustainable_daily_capacity = 8  # tasks per day
        self.focus_hours_per_day = 6
        self.completion_rate = 0.8
        
        # Project priority weights (dynamic)
        self.project_weights = {
            Project.AGENTFORCE: 0.5,
            Project.REDDIT: 0.2,
            Project.WEBSITE: 0.3
        }
        
    def analyze_current_workload(self, tasks: List[Task]) -> Dict[str, Any]:
        """Analyze current task distribution and identify problems"""
        
        today = datetime.date.today()
        overdue_tasks = [t for t in tasks if t.due_date < today]
        due_today = [t for t in tasks if t.due_date == today]
        upcoming_tasks = [t for t in tasks if t.due_date > today]
        
        analysis = {
            'total_tasks': len(tasks),
            'overdue_count': len(overdue_tasks),
            'due_today_count': len(due_today),
            'upcoming_count': len(upcoming_tasks),
            'project_distribution': self._get_project_distribution(tasks),
            'estimated_hours_today': sum(t.estimated_hours for t in due_today),
            'capacity_utilization': len(due_today) / self.sustainable_daily_capacity,
            'risk_level': self._calculate_risk_level(due_today, overdue_tasks)
        }
        
        return analysis
    
    def smart_task_filter(self, tasks: List[Task], user_energy_level: int = 3) -> List[Task]:
        """Intelligent filtering based on multiple factors"""
        
        today = datetime.date.today()
        filtered_tasks = []
        
        for task in tasks:
            # Calculate priority score
            score = self._calculate_priority_score(task, user_energy_level)
            
            # Apply filtering criteria
            if (score >= 0.6 and  # Minimum priority threshold
                task.energy_required <= user_energy_level + 1 and  # Energy match
                self._has_dependencies_met(task, tasks)):
                
                filtered_tasks.append((task, score))
        
        # Sort by priority score and return top N
        filtered_tasks.sort(key=lambda x: x[1], reverse=True)
        
        # Limit to sustainable daily capacity
        max_tasks = int(self.sustainable_daily_capacity * self.completion_rate)
        return [task for task, _ in filtered_tasks[:max_tasks]]
    
    def auto_reschedule_overdue(self, tasks: List[Task]) -> List[Task]:
        """Intelligent rescheduling of overdue tasks"""
        
        today = datetime.date.today()
        rescheduled_tasks = []
        
        for task in tasks:
            if task.due_date < today:
                # Calculate optimal new date
                new_date = self._find_optimal_reschedule_date(task, tasks)
                
                # Create updated task
                updated_task = Task(
                    id=task.id,
                    title=task.title,
                    project=task.project,
                    due_date=new_date,
                    estimated_hours=task.estimated_hours,
                    priority=task.priority,
                    energy_required=task.energy_required,
                    dependencies=task.dependencies,
                    created_date=task.created_date
                )
                
                rescheduled_tasks.append(updated_task)
            else:
                rescheduled_tasks.append(task)
        
        return rescheduled_tasks
    
    def generate_daily_plan(self, tasks: List[Task], user_energy_level: int = 3) -> Dict[str, Any]:
        """Generate optimized daily task plan"""
        
        # Filter tasks for today
        today = datetime.date.today()
        available_tasks = [t for t in tasks if t.due_date <= today]
        
        # Apply smart filtering
        prioritized_tasks = self.smart_task_filter(available_tasks, user_energy_level)
        
        # Group by energy level and project
        energy_groups = self._group_by_energy_level(prioritized_tasks)
        project_groups = self._group_by_project(prioritized_tasks)
        
        # Create time-blocked schedule
        schedule = self._create_time_blocks(energy_groups, user_energy_level)
        
        return {
            'date': today.isoformat(),
            'total_tasks': len(prioritized_tasks),
            'estimated_hours': sum(t.estimated_hours for t in prioritized_tasks),
            'tasks_by_priority': self._group_by_priority(prioritized_tasks),
            'tasks_by_project': project_groups,
            'energy_distribution': energy_groups,
            'schedule': schedule,
            'completion_probability': self._calculate_completion_probability(prioritized_tasks)
        }
    
    def _calculate_priority_score(self, task: Task, user_energy_level: int) -> float:
        """Calculate comprehensive priority score"""
        
        today = datetime.date.today()
        days_overdue = max(0, (today - task.due_date).days)
        
        # Base priority score
        base_score = 1.0 / task.priority.value
        
        # Due date urgency (exponential decay)
        urgency_score = min(1.0, days_overdue / 7) * 0.3
        
        # Project weight
        project_score = self.project_weights.get(task.project, 0.1)
        
        # Energy match bonus
        energy_match = max(0, 1 - abs(task.energy_required - user_energy_level) / 5)
        
        # Time estimation factor (prefer smaller tasks when overloaded)
        time_factor = max(0.1, 1 - task.estimated_hours / 8)
        
        # Age factor (older tasks get slight boost)
        days_old = (today - task.created_date).days
        age_factor = min(0.2, days_old / 30)
        
        total_score = (
            base_score * 0.4 +
            urgency_score * 0.25 +
            project_score * 0.2 +
            energy_match * 0.1 +
            time_factor * 0.05
        ) + age_factor
        
        return min(1.0, total_score)
    
    def _find_optimal_reschedule_date(self, task: Task, all_tasks: List[Task]) -> datetime.date:
        """Find optimal date considering capacity and dependencies"""
        
        today = datetime.date.today()
        
        # Start with minimum delay based on task complexity
        min_delay = max(1, int(task.estimated_hours / 2))
        candidate_date = today + datetime.timedelta(days=min_delay)
        
        # Find first available slot with capacity
        while True:
            # Check capacity on candidate date
            tasks_on_date = [t for t in all_tasks if t.due_date == candidate_date]
            total_hours = sum(t.estimated_hours for t in tasks_on_date)
            
            if (len(tasks_on_date) < self.sustainable_daily_capacity and
                total_hours + task.estimated_hours <= self.focus_hours_per_day):
                break
            
            candidate_date += datetime.timedelta(days=1)
            
            # Safety check - don't schedule too far out
            if (candidate_date - today).days > 30:
                candidate_date = today + datetime.timedelta(days=7)
                break
        
        return candidate_date
    
    def _get_project_distribution(self, tasks: List[Task]) -> Dict[str, int]:
        """Get task count by project"""
        distribution = {}
        for project in Project:
            distribution[project.value] = len([t for t in tasks if t.project == project])
        return distribution
    
    def _calculate_risk_level(self, due_today: List[Task], overdue: List[Task]) -> str:
        """Calculate workload risk level"""
        
        total_due = len(due_today) + len(overdue)
        
        if total_due > self.sustainable_daily_capacity * 1.5:
            return "CRITICAL"
        elif total_due > self.sustainable_daily_capacity:
            return "HIGH"
        elif total_due > self.sustainable_daily_capacity * 0.8:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _has_dependencies_met(self, task: Task, all_tasks: List[Task]) -> bool:
        """Check if task dependencies are completed"""
        # Simplified - in real implementation would check completion status
        return True
    
    def _group_by_energy_level(self, tasks: List[Task]) -> Dict[int, List[Task]]:
        """Group tasks by required energy level"""
        groups = {i: [] for i in range(1, 6)}
        for task in tasks:
            groups[task.energy_required].append(task)
        return groups
    
    def _group_by_project(self, tasks: List[Task]) -> Dict[str, List[Task]]:
        """Group tasks by project"""
        groups = {project.value: [] for project in Project}
        for task in tasks:
            groups[task.project.value].append(task)
        return groups
    
    def _group_by_priority(self, tasks: List[Task]) -> Dict[str, List[Task]]:
        """Group tasks by priority level"""
        groups = {priority.name: [] for priority in Priority}
        for task in tasks:
            groups[task.priority.name].append(task)
        return groups
    
    def _create_time_blocks(self, energy_groups: Dict[int, List[Task]], 
                           user_energy_level: int) -> List[Dict[str, Any]]:
        """Create time-blocked schedule"""
        
        schedule = []
        current_time = 9  # Start at 9 AM
        
        # Schedule high-energy tasks when user energy is high
        for energy_level in sorted(energy_groups.keys(), reverse=True):
            if energy_level <= user_energy_level and energy_groups[energy_level]:
                for task in energy_groups[energy_level][:2]:  # Max 2 per energy level
                    duration = max(1, int(task.estimated_hours))
                    
                    schedule.append({
                        'time': f"{current_time:02d}:00 - {current_time + duration:02d}:00",
                        'task': task.title,
                        'project': task.project.value,
                        'energy_level': energy_level,
                        'priority': task.priority.name
                    })
                    
                    current_time += duration
                    if current_time >= 17:  # Stop by 5 PM
                        break
        
        return schedule
    
    def _calculate_completion_probability(self, tasks: List[Task]) -> float:
        """Calculate probability of completing all tasks"""
        
        total_hours = sum(t.estimated_hours for t in tasks)
        task_count = len(tasks)
        
        # Based on historical completion rates and current load
        time_probability = min(1.0, self.focus_hours_per_day / max(total_hours, 1))
        count_probability = min(1.0, self.sustainable_daily_capacity / max(task_count, 1))
        
        return (time_probability * 0.6 + count_probability * 0.4) * self.completion_rate

# Example usage and testing
def main():
    """Test the optimization system with sample data"""
    
    optimizer = AsanaOptimizer()
    
    # Sample task data (simulating Kobi's current workload)
    sample_tasks = [
        Task("1", "Fix Agentforce login bug", Project.AGENTFORCE, 
             datetime.date.today(), 2, Priority.CRITICAL, 4, [], 
             datetime.date.today() - datetime.timedelta(days=2)),
        
        Task("2", "Review Reddit community guidelines", Project.REDDIT, 
             datetime.date.today(), 1, Priority.MEDIUM, 2, [], 
             datetime.date.today() - datetime.timedelta(days=1)),
        
        Task("3", "Update website FAQ section", Project.WEBSITE, 
             datetime.date.today(), 3, Priority.HIGH, 3, [], 
             datetime.date.today() - datetime.timedelta(days=3)),
        
        Task("4", "Agentforce performance optimization", Project.AGENTFORCE, 
             datetime.date.today() - datetime.timedelta(days=1), 4, Priority.HIGH, 5, [], 
             datetime.date.today() - datetime.timedelta(days=5)),
        
        Task("5", "Reddit engagement analytics", Project.REDDIT, 
             datetime.date.today() - datetime.timedelta(days=2), 2, Priority.MEDIUM, 3, [], 
             datetime.date.today() - datetime.timedelta(days=4)),
    ]
    
    # Analyze current workload
    print("=== CURRENT WORKLOAD ANALYSIS ===")
    analysis = optimizer.analyze_current_workload(sample_tasks)
    print(json.dumps(analysis, indent=2, default=str))
    
    # Generate daily plan
    print("\n=== OPTIMIZED DAILY PLAN ===")
    daily_plan = optimizer.generate_daily_plan(sample_tasks, user_energy_level=3)
    print(json.dumps(daily_plan, indent=2, default=str))
    
    # Auto-reschedule overdue tasks
    print("\n=== RESCHEDULED TASKS ===")
    rescheduled = optimizer.auto_reschedule_overdue(sample_tasks)
    for task in rescheduled:
        if task.due_date > datetime.date.today():
            print(f"Rescheduled: {task.title} -> {task.due_date}")

if __name__ == "__main__":
    main()