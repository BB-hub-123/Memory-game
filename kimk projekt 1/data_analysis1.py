import json
import os
from datetime import datetime

def load_experiment_files():
    """Find and load all experiment JSON files"""
    
    # Define what files to look for
    experiment_patterns = {
        'Experiment 1 - Primacy & Recency': 'primacy_recency_results_',
        'Experiment 2 - Presentation Speed': 'experiment2_presentation_speed_',
        'Experiment 3 - Working Memory Task': 'experiment3_working_memory_task_',
        'Experiment 4 - Pause Before Recall': 'delayed_memory_results_',
        'Experiment 5 - Working Memory Capacity': 'experiment5_working_memory_capacity_',
        'Experiment 6 - Chunking': 'experiment6_chunking_',
        'Experiment 7 - Articulatory Suppression': 'experiment7_articulatory_suppression_',
        'Experiment 8 - Finger Tapping': 'experiment8_finger_tapping_'
    }
    
    experiments = {}
    
    # Look for files in current directory
    files_found = os.listdir('.')
    
    for exp_name, pattern in experiment_patterns.items():
        matching_files = [f for f in files_found if f.startswith(pattern) and f.endswith('.json')]
        
        if matching_files:
            # Load all matching files
            all_data = []
            for file in matching_files:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        all_data.extend(data)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            if all_data:
                experiments[exp_name] = all_data
                print(f"✓ Found {exp_name}: {len(all_data)} participants")
        else:
            print(f"✗ No data found for {exp_name}")
    
    return experiments

def display_experiment_1(data):
    """Display Experiment 1: Primacy & Recency data"""
    print("\n" + "="*60)
    print("EXPERIMENT 1: PRIMACY & RECENCY EFFECTS")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        analysis = participant['analysis']
        
        print(f"\nParticipant: {name}")
        print(f"  Total recalled: {analysis['total_recalled']}/20")
        print(f"  Primacy (pos 1-5):  {analysis['primacy_score']:.1%}")
        print(f"  Middle (pos 6-15):  {analysis['middle_score']:.1%}")
        print(f"  Recency (pos 16-20): {analysis['recency_score']:.1%}")
        
        # Show which positions were recalled
        recalled = analysis['position_data']
        positions_recalled = [str(i+1) for i, pos in enumerate(recalled) if pos['recalled']]
        print(f"  Positions recalled: {', '.join(positions_recalled)}")

def display_experiment_2(data):
    """Display Experiment 2: Presentation Speed data"""
    print("\n" + "="*60)
    print("EXPERIMENT 2: PRESENTATION SPEED EFFECTS")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        conditions = participant['conditions']
        
        print(f"\nParticipant: {name}")
        print(f"  Slow condition (1s/letter):  {conditions['slow']['analysis']['recall_rate']:.1%}")
        print(f"  Fast condition (0.5s/letter): {conditions['fast']['analysis']['recall_rate']:.1%}")
        
        speed_effect = conditions['slow']['analysis']['recall_rate'] - conditions['fast']['analysis']['recall_rate']
        print(f"  Speed benefit: {speed_effect:+.1%}")

def display_experiment_3(data):
    """Display Experiment 3: Working Memory Task data"""
    print("\n" + "="*60)
    print("EXPERIMENT 3: WORKING MEMORY TASK AFTER LIST")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        conditions = participant['conditions']
        distraction = participant['distraction_performance']
        
        print(f"\nParticipant: {name}")
        print(f"  Control condition:     {conditions['control']['analysis']['recall_rate']:.1%}")
        print(f"  Distraction condition: {conditions['distraction']['analysis']['recall_rate']:.1%}")
        
        if distraction:
            print(f"  Distraction task: {distraction['numbers_entered']} numbers, {distraction['correct_sequence']} correct")
        
        effect = conditions['control']['analysis']['recall_rate'] - conditions['distraction']['analysis']['recall_rate']
        print(f"  Working memory effect: {effect:+.1%}")

def display_experiment_4(data):
    """Display Experiment 4: Pause Before Recall data"""
    print("\n" + "="*60)
    print("EXPERIMENT 4: PAUSE BEFORE RECALL (60s delay)")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        answers = participant['answers']
        score = participant['score']
        accuracy = participant['accuracy']
        
        print(f"\nParticipant: {name}")
        print(f"  Score: {score}/20 ({accuracy:.1f}%)")
        print(f"  Delay: 60 seconds between sequence and recall")
        
        # Show first few answers
        correct_positions = [str(ans['position']) for ans in answers[:5] if ans['is_correct']]
        print(f"  First 5 positions correct: {', '.join(correct_positions) if correct_positions else 'None'}")

def display_experiment_5(data):
    """Display Experiment 5: Working Memory Capacity data"""
    print("\n" + "="*60)
    print("EXPERIMENT 5: WORKING MEMORY CAPACITY")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        capacity = participant['capacity_analysis']
        
        print(f"\nParticipant: {name}")
        print(f"  Estimated capacity: {capacity['estimated_capacity']} items")
        print(f"  Longest perfect recall: {capacity['max_perfect_length']} items")
        
        # Show performance by length
        print("  Performance by length:")
        for length, accuracy in sorted(capacity['performance_by_length'].items()):
            print(f"    {length} items: {accuracy:.1%}")

def display_experiment_6(data):
    """Display Experiment 6: Chunking data"""
    print("\n" + "="*60)
    print("EXPERIMENT 6: CHUNKING EFFECTS")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        analysis = participant['chunking_analysis']
        
        print(f"\nParticipant: {name}")
        print(f"  Chunkable sequences: {analysis['chunkable_accuracy']:.1%}")
        print(f"  Random sequences:    {analysis['random_accuracy']:.1%}")
        print(f"  Chunking benefit:    {analysis['chunking_benefit']:+.1%}")
        print(f"  Chunks recalled intact: {analysis['chunks_intact']}/{analysis['total_chunkable_trials']}")

def display_experiment_7(data):
    """Display Experiment 7: Articulatory Suppression data"""
    print("\n" + "="*60)
    print("EXPERIMENT 7: ARTICULATORY SUPPRESSION")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        analysis = participant['suppression_analysis']
        
        print(f"\nParticipant: {name}")
        print(f"  Control condition:     {analysis['control_accuracy']:.1%}")
        print(f"  Suppression condition: {analysis['suppression_accuracy']:.1%}")
        print(f"  Suppression effect:    {analysis['accuracy_effect']:+.1%}")
        print(f"  Span effect: {analysis['span_effect']:+.1f} items")

def display_experiment_8(data):
    """Display Experiment 8: Finger Tapping data"""
    print("\n" + "="*60)
    print("EXPERIMENT 8: FINGER TAPPING")
    print("="*60)
    
    for participant in data:
        name = participant['name']
        analysis = participant['tapping_analysis']
        
        print(f"\nParticipant: {name}")
        print(f"  Control condition: {analysis['control_accuracy']:.1%}")
        print(f"  Tapping condition: {analysis['tapping_accuracy']:.1%}")
        print(f"  Tapping effect:    {analysis['accuracy_effect']:+.1%}")
        print(f"  Span effect: {analysis['span_effect']:+.1f} items")

def create_summary_table(experiments):
    """Create a summary table of all participants across experiments"""
    print("\n" + "="*80)
    print("SUMMARY TABLE - ALL EXPERIMENTS")
    print("="*80)
    
    # Collect all unique participant names
    all_participants = set()
    for exp_data in experiments.values():
        for participant in exp_data:
            all_participants.add(participant['name'])
    
    print(f"\nTotal unique participants: {len(all_participants)}")
    print(f"Participants: {', '.join(sorted(all_participants))}")
    
    # Show which experiments each participant completed
    print(f"\nParticipant completion matrix:")
    print(f"{'Participant':<15}", end='')
    for exp_name in experiments.keys():
        exp_short = exp_name.split(' - ')[0]  # Just "Experiment 1", etc.
        print(f"{exp_short:<8}", end='')
    print()
    
    for participant_name in sorted(all_participants):
        print(f"{participant_name:<15}", end='')
        for exp_data in experiments.values():
            participant_names = [p['name'] for p in exp_data]
            if participant_name in participant_names:
                print(f"{'✓':<8}", end='')
            else:
                print(f"{'✗':<8}", end='')
        print()

def main():
    """Main function to display all experiment data"""
    print("MEMORY EXPERIMENT DATA VIEWER")
    print("Loading all experiment files...")
    
    # Load all experiments
    experiments = load_experiment_files()
    
    if not experiments:
        print("No experiment data files found!")
        print("Make sure your JSON files are in the same folder as this script.")
        return
    
    print(f"\nTotal experiments loaded: {len(experiments)}")
    
    # Display functions for each experiment
    display_functions = {
        'Experiment 1 - Primacy & Recency': display_experiment_1,
        'Experiment 2 - Presentation Speed': display_experiment_2,
        'Experiment 3 - Working Memory Task': display_experiment_3,
        'Experiment 4 - Pause Before Recall': display_experiment_4,
        'Experiment 5 - Working Memory Capacity': display_experiment_5,
        'Experiment 6 - Chunking': display_experiment_6,
        'Experiment 7 - Articulatory Suppression': display_experiment_7,
        'Experiment 8 - Finger Tapping': display_experiment_8
    }
    
    # Display each experiment's data
    for exp_name, exp_data in experiments.items():
        if exp_name in display_functions:
            display_functions[exp_name](exp_data)
    
    # Create summary table
    create_summary_table(experiments)
    
    # Export option
    print(f"\n" + "="*80)
    print("EXPORT OPTIONS")
    print("="*80)
    print("This script showed you all your data in readable format.")
    print("To export data for further analysis:")
    print("1. Copy the output above")
    print("2. Use pandas to create CSV files:")
    print("   import pandas as pd")
    print("   # Create DataFrames from the JSON data")
    print("3. Use matplotlib/seaborn for graphs")
    print("4. Use scipy.stats for statistical tests")

if __name__ == "__main__":
    main()