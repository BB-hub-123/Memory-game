import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 8: Finger Tapping")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 100)

def get_text_input(screen, prompt):
    """Simple text input function"""
    text = ""
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        
        screen.fill(WHITE)
        
        prompt_surface = font_medium.render(prompt, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(400, 250))
        screen.blit(prompt_surface, prompt_rect)
        
        text_surface = font_medium.render(text + "|", True, BLACK)
        text_rect = text_surface.get_rect(center=(400, 320))
        screen.blit(text_surface, text_rect)
        
        instruction = font_small.render("Press ENTER to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 400))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
    
    return text.strip()

def generate_consonant_sequence(length):
    """Generate a sequence of random consonants"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'  # Exclude vowels
    return [random.choice(consonants) for _ in range(length)]

def show_sequence_with_tapping(screen, letters, trial_num, condition, sequence_length):
    """Show sequence with or without finger tapping"""
    print(f"Starting {condition} sequence of length {sequence_length} (trial {trial_num})...")
    
    tapping_active = (condition == "tapping")
    
    if tapping_active:
        # Show tapping instructions
        screen.fill(WHITE)
        tapping_title = font_medium.render("FINGER TAPPING", True, BLUE)
        tapping_rect = tapping_title.get_rect(center=(400, 150))
        screen.blit(tapping_title, tapping_rect)
        
        instruction1 = font_small.render("Tap your finger continuously on the desk", True, BLACK)
        instruction1_rect = instruction1.get_rect(center=(400, 200))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Keep tapping at a steady rhythm during the entire sequence", True, BLACK)
        instruction2_rect = instruction2.get_rect(center=(400, 230))
        screen.blit(instruction2, instruction2_rect)
        
        instruction3 = font_small.render("This tests motor vs verbal working memory interference", True, GRAY)
        instruction3_rect = instruction3.get_rect(center=(400, 280))
        screen.blit(instruction3, instruction3_rect)
        
        ready_text = font_small.render("Start tapping and press any key", True, BLUE)
        ready_rect = ready_text.get_rect(center=(400, 350))
        screen.blit(ready_text, ready_rect)
        
        pygame.display.flip()
        
        # Wait for ready
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
    
    # Show letters one by one
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show condition and trial info
        if tapping_active:
            condition_text = font_small.render("KEEP TAPPING YOUR FINGER", True, BLUE)
            screen.blit(condition_text, (20, 20))
        else:
            condition_text = font_small.render(f"CONTROL - Trial {trial_num}", True, BLACK)
            screen.blit(condition_text, (20, 20))
        
        # Show sequence progress
        progress_text = font_small.render(f"Letter {i+1}/{sequence_length}", True, GRAY)
        screen.blit(progress_text, (20, 50))
        
        # Show the letter
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        # Reminder for tapping condition
        if tapping_active:
            reminder = font_medium.render("*tap* *tap* *tap*", True, BLUE)
            reminder_rect = reminder.get_rect(center=(400, 450))
            screen.blit(reminder, reminder_rect)
        
        pygame.display.flip()
        time.sleep(1)  # 1 second per letter
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    # Stop tapping reminder
    if tapping_active:
        screen.fill(WHITE)
        stop_text = font_medium.render("STOP tapping", True, GREEN)
        stop_rect = stop_text.get_rect(center=(400, 250))
        screen.blit(stop_text, stop_rect)
        
        ready_text = font_small.render("Now prepare to recall the letters", True, BLACK)
        ready_rect = ready_text.get_rect(center=(400, 320))
        screen.blit(ready_text, ready_rect)
        
        pygame.display.flip()
        time.sleep(2)

def get_serial_recall_input(screen, participant_name, sequence_length, trial_num, condition):
    """Get serial recall input from participant"""
    recalled_letters = []
    current_input = ""
    
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_input.strip():
                        letter = current_input.strip().upper()
                        if len(letter) == 1 and letter.isalpha():
                            recalled_letters.append(letter)
                            current_input = ""
                            
                            if len(recalled_letters) >= sequence_length:
                                input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if current_input:
                        current_input = current_input[:-1]
                    elif recalled_letters:
                        recalled_letters.pop()
                elif event.key == pygame.K_SPACE:
                    if current_input.strip():
                        letter = current_input.strip().upper()
                        if len(letter) == 1 and letter.isalpha():
                            recalled_letters.append(letter)
                            current_input = ""
                            
                            if len(recalled_letters) >= sequence_length:
                                input_active = False
                elif len(current_input) < 1 and event.unicode.isalpha():
                    current_input = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Recall Letters - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        trial_info = font_small.render(f"Trial {trial_num} ({condition}) - Enter {sequence_length} letters in order", True, BLACK)
        trial_rect = trial_info.get_rect(center=(400, 130))
        screen.blit(trial_info, trial_rect)
        
        # Emphasize that tapping should stop during recall
        if condition == "tapping":
            emphasis = font_small.render("(Do NOT tap during recall)", True, BLUE)
            emphasis_rect = emphasis.get_rect(center=(400, 155))
            screen.blit(emphasis, emphasis_rect)
        
        instruction1 = font_small.render("Type each letter and press ENTER or SPACE", True, GRAY)
        instruction1_rect = instruction1.get_rect(center=(400, 185))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Backspace to remove letters", True, GRAY)
        instruction2_rect = instruction2.get_rect(center=(400, 210))
        screen.blit(instruction2, instruction2_rect)
        
        # Current input
        input_label = font_small.render(f"Position {len(recalled_letters) + 1}:", True, BLACK)
        screen.blit(input_label, (250, 270))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        input_rect = input_surface.get_rect(center=(400, 320))
        screen.blit(input_surface, input_rect)
        
        # Show sequence entered so far
        sequence_label = font_small.render(f"Sequence entered ({len(recalled_letters)}/{sequence_length}):", True, BLACK)
        screen.blit(sequence_label, (50, 400))
        
        # Display letters in sequence
        x_start = 50
        y_start = 440
        
        for i in range(sequence_length):
            x = x_start + i * 60
            
            # Draw position box
            box_color = GREEN if i < len(recalled_letters) else GRAY
            pygame.draw.rect(screen, box_color, (x, y_start, 50, 50), 3)
            
            # Draw position number
            pos_text = font_small.render(str(i + 1), True, BLACK)
            screen.blit(pos_text, (x + 20, y_start - 25))
            
            # Draw letter if entered
            if i < len(recalled_letters):
                letter_surface = font_medium.render(recalled_letters[i], True, BLACK)
                letter_rect = letter_surface.get_rect(center=(x + 25, y_start + 25))
                screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
    
    # Pad with empty strings if too short
    while len(recalled_letters) < sequence_length:
        recalled_letters.append("")
    
    return recalled_letters[:sequence_length]

def analyze_tapping_effect(recalled_letters, original_letters):
    """Analyze serial recall performance"""
    
    # Position-by-position accuracy
    position_accuracy = []
    correct_positions = 0
    
    for i in range(len(original_letters)):
        if i < len(recalled_letters):
            correct = recalled_letters[i] == original_letters[i]
            position_accuracy.append(correct)
            if correct:
                correct_positions += 1
        else:
            position_accuracy.append(False)
    
    # Calculate sequence length correctly recalled (from start)
    correct_from_start = 0
    for i in range(len(original_letters)):
        if i < len(recalled_letters) and recalled_letters[i] == original_letters[i]:
            correct_from_start += 1
        else:
            break
    
    results = {
        'original_sequence': original_letters,
        'recalled_sequence': recalled_letters,
        'correct_positions': correct_positions,
        'total_positions': len(original_letters),
        'position_accuracy': position_accuracy,
        'accuracy_rate': correct_positions / len(original_letters),
        'correct_from_start': correct_from_start
    }
    
    return results

def show_trial_results(screen, participant_name, analysis, trial_num, condition):
    """Show results for individual trial"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Trial {trial_num} Results - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Condition info
        condition_text = font_small.render(f"Condition: {condition.upper()}", True, BLUE)
        screen.blit(condition_text, (50, 100))
        
        # Trial summary
        score_text = font_small.render(f"Score: {analysis['correct_positions']}/{analysis['total_positions']} positions correct ({analysis['accuracy_rate']*100:.1f}%)", True, BLACK)
        screen.blit(score_text, (50, 130))
        
        span_text = font_small.render(f"Correct from start: {analysis['correct_from_start']} letters", True, BLACK)
        screen.blit(span_text, (50, 160))
        
        # Show sequences
        y_pos = 210
        original_label = font_small.render("Original sequence:", True, BLACK)
        screen.blit(original_label, (50, y_pos))
        
        y_pos += 30
        for i, letter in enumerate(analysis['original_sequence']):
            x = 50 + i * 60
            
            # Background for original
            pygame.draw.rect(screen, BLUE, (x, y_pos, 50, 50), 3)
            
            letter_surface = font_medium.render(letter, True, BLACK)
            letter_rect = letter_surface.get_rect(center=(x + 25, y_pos + 25))
            screen.blit(letter_surface, letter_rect)
        
        y_pos += 80
        recalled_label = font_small.render("Your recall:", True, BLACK)
        screen.blit(recalled_label, (50, y_pos))
        
        y_pos += 30
        for i, letter in enumerate(analysis['recalled_sequence']):
            x = 50 + i * 60
            
            # Color based on correctness
            if analysis['position_accuracy'][i]:
                color = GREEN
            else:
                color = RED
            
            pygame.draw.rect(screen, color, (x, y_pos, 50, 50), 3)
            
            if letter:  # Only show if not empty
                letter_surface = font_medium.render(letter, True, BLACK)
                letter_rect = letter_surface.get_rect(center=(x + 25, y_pos + 25))
                screen.blit(letter_surface, letter_rect)
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def analyze_finger_tapping_experiment(all_trials):
    """Analyze overall finger tapping effect"""
    
    control_trials = [t for t in all_trials if t['condition'] == 'control']
    tapping_trials = [t for t in all_trials if t['condition'] == 'tapping']
    
    # Calculate average performance by condition
    control_accuracy = sum(t['analysis']['accuracy_rate'] for t in control_trials) / len(control_trials) if control_trials else 0
    tapping_accuracy = sum(t['analysis']['accuracy_rate'] for t in tapping_trials) / len(tapping_trials) if tapping_trials else 0
    
    # Calculate average span (correct from start) by condition
    control_span = sum(t['analysis']['correct_from_start'] for t in control_trials) / len(control_trials) if control_trials else 0
    tapping_span = sum(t['analysis']['correct_from_start'] for t in tapping_trials) / len(tapping_trials) if tapping_trials else 0
    
    # Calculate tapping effect (should be minimal according to theory)
    accuracy_effect = control_accuracy - tapping_accuracy
    span_effect = control_span - tapping_span
    
    # Performance by sequence length
    length_performance = {'control': {}, 'tapping': {}}
    
    for trial in all_trials:
        condition = trial['condition']
        length = trial['sequence_length']
        accuracy = trial['analysis']['accuracy_rate']
        
        if length not in length_performance[condition]:
            length_performance[condition][length] = []
        length_performance[condition][length].append(accuracy)
    
    # Average by length
    for condition in length_performance:
        for length in length_performance[condition]:
            accuracies = length_performance[condition][length]
            length_performance[condition][length] = sum(accuracies) / len(accuracies)
    
    results = {
        'control_accuracy': control_accuracy,
        'tapping_accuracy': tapping_accuracy,
        'accuracy_effect': accuracy_effect,
        'control_span': control_span,
        'tapping_span': tapping_span,
        'span_effect': span_effect,
        'length_performance': length_performance,
        'total_control_trials': len(control_trials),
        'total_tapping_trials': len(tapping_trials)
    }
    
    return results

def show_final_results(screen, participant_name, tapping_analysis, all_trials):
    """Show final finger tapping results"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Finger Tapping Results - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Main comparison
        y_pos = 120
        comparison_header = font_small.render("Overall Performance Comparison:", True, BLACK)
        screen.blit(comparison_header, (50, y_pos))
        
        y_pos += 30
        headers = ["Condition", "Accuracy", "Avg Span", "Effect"]
        header_text = font_small.render(f"{headers[0]:<12} {headers[1]:<10} {headers[2]:<10} {headers[3]}", True, BLACK)
        screen.blit(header_text, (50, y_pos))
        
        y_pos += 20
        pygame.draw.line(screen, BLACK, (50, y_pos), (400, y_pos), 2)
        y_pos += 10
        
        # Control condition
        control_text = f"Control      {tapping_analysis['control_accuracy']*100:>6.1f}%   {tapping_analysis['control_span']:>6.1f}     --"
        control_surface = font_small.render(control_text, True, BLACK)
        screen.blit(control_surface, (50, y_pos))
        
        y_pos += 20
        
        # Tapping condition
        tapping_text = f"Tapping      {tapping_analysis['tapping_accuracy']*100:>6.1f}%   {tapping_analysis['tapping_span']:>6.1f}   {tapping_analysis['accuracy_effect']*100:>+5.1f}%"
        tapping_surface = font_small.render(tapping_text, True, BLACK)
        screen.blit(tapping_surface, (50, y_pos))
        
        # Effect interpretation
        y_pos += 50
        interpretation = font_small.render("Finger Tapping Effect:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        if abs(tapping_analysis['accuracy_effect']) < 0.05:
            effect_text = "✓ No significant effect - motor/verbal systems independent!"
            effect_color = GREEN
        elif tapping_analysis['accuracy_effect'] > 0.1:
            effect_text = "⚠ Unexpected large effect from finger tapping"
            effect_color = RED
        else:
            effect_text = "~ Small effect detected"
            effect_color = BLUE
        
        effect_surface = font_small.render(effect_text, True, effect_color)
        screen.blit(effect_surface, (50, y_pos))
        
        y_pos += 25
        if abs(tapping_analysis['span_effect']) < 0.3:
            span_text = "✓ Memory span largely unaffected by tapping"
            span_color = GREEN
        else:
            span_text = "~ Some effect on memory span"
            span_color = BLUE
        
        span_surface = font_small.render(span_text, True, span_color)
        screen.blit(span_surface, (50, y_pos))
        
        # Comparison with articulatory suppression theory
        y_pos += 50
        comparison_header = font_small.render("Theory Comparison:", True, BLACK)
        screen.blit(comparison_header, (50, y_pos))
        
        y_pos += 25
        theory_points = [
            "Articulatory suppression should strongly affect verbal memory",
            "Finger tapping should have minimal effect (different systems)",
            f"Your results: {abs(tapping_analysis['accuracy_effect']*100):.1f}% effect from tapping"
        ]
        
        for point in theory_points:
            point_surface = font_small.render(point, True, GRAY)
            screen.blit(point_surface, (50, y_pos))
            y_pos += 20
        
        # Performance by length (if enough data)
        if len(tapping_analysis['length_performance']['control']) > 1:
            y_pos += 30
            length_header = font_small.render("Performance by Sequence Length:", True, BLACK)
            screen.blit(length_header, (50, y_pos))
            
            y_pos += 25
            for length in sorted(tapping_analysis['length_performance']['control'].keys()):
                if length in tapping_analysis['length_performance']['tapping']:
                    control_perf = tapping_analysis['length_performance']['control'][length]
                    tapping_perf = tapping_analysis['length_performance']['tapping'][length]
                    diff = control_perf - tapping_perf
                    
                    length_text = f"Length {length}: Control {control_perf*100:.1f}% vs Tapping {tapping_perf*100:.1f}% (Δ{diff*100:+.1f}%)"
                    color = RED if abs(diff) > 0.1 else GRAY
                    
                    length_surface = font_small.render(length_text, True, color)
                    screen.blit(length_surface, (50, y_pos))
                    y_pos += 20
        
        # Theory explanation
        y_pos += 20
        theory_label = font_small.render("Theory:", True, BLACK)
        screen.blit(theory_label, (50, y_pos))
        
        y_pos += 20
        theory_text = [
            "Working memory has separate verbal and motor components",
            "Finger tapping uses motor resources, not verbal phonological loop",
            "Should NOT interfere with verbal memory (unlike 'ta-ta-ta')"
        ]
        
        for text in theory_text:
            theory_surface = font_small.render(text, True, GRAY)
            screen.blit(theory_surface, (50, y_pos))
            y_pos += 18
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment8_finger_tapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"Data saved to {filename}")

def main():
    """Main experiment loop"""
    all_results = []
    
    while True:
        participant_name = get_text_input(screen, "Enter participant name (or 'quit' to exit):")
        
        if participant_name.lower() == 'quit':
            break
        
        if not participant_name:
            continue
        
        # Show instructions
        screen.fill(WHITE)
        title = font_medium.render("Experiment 8: Finger Tapping", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instructions = [
            "This experiment tests motor vs verbal working memory interference:",
            "",
            "You'll complete MULTIPLE trials with TWO types:",
            "",
            "CONTROL trials:",
            "• See random consonant sequences normally",
            "• Use any memory strategy you want",
            "",
            "TAPPING trials:", 
            "• Tap your finger continuously on the desk during letters",
            "• Keep a steady rhythm throughout presentation",
            "• Stop tapping when letters finish",
            "",
            "You'll do 20 trials total (10 of each type) with random sequences.",
            "Theory: Finger tapping should NOT affect verbal memory",
            "because motor and verbal systems are separate",
            "",
            "Press any key to start"
        ]
        
        y_pos = 120
        for instruction in instructions:
            color = BLUE if instruction.startswith("Press") else BLACK
            if instruction == "":
                y_pos += 10
                continue
            text = font_small.render(instruction, True, color)
            screen.blit(text, (50, y_pos))
            y_pos += 22
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        
        # Run trials with both conditions - 20 trials total
        trials_per_condition = 10  # 10 control + 10 tapping = 20 total
        conditions = ['control', 'tapping']
        
        # Create trial list
        trial_list = []
        for condition in conditions:
            for trial in range(trials_per_condition):
                trial_list.append(condition)
        
        # Randomize order
        random.shuffle(trial_list)
        
        results = {'control': [], 'tapping': []}
        trial_num = 1
        
        for condition in trial_list:
            # Generate new random sequence for each trial
            length = 6  # Use 6-letter sequences for better comparison
            letters = generate_consonant_sequence(length)
            
            # Show trial introduction
            screen.fill(WHITE)
            trial_intro = font_medium.render(f"Trial {trial_num}/20: {condition.upper()} condition", True, BLACK)
            trial_rect = trial_intro.get_rect(center=(400, 200))
            screen.blit(trial_intro, trial_rect)
            
            length_text = font_small.render(f"Sequence length: {length} letters", True, GRAY)
            length_rect = length_text.get_rect(center=(400, 250))
            screen.blit(length_text, length_rect)
            
            if condition == "tapping":
                reminder = font_small.render("Remember: Tap your finger continuously during letters", True, BLUE)
                reminder_rect = reminder.get_rect(center=(400, 300))
                screen.blit(reminder, reminder_rect)
            
            ready_text = font_small.render("Press any key when ready", True, BLUE)
            ready_rect = ready_text.get_rect(center=(400, 350))
            screen.blit(ready_text, ready_rect)
            
            pygame.display.flip()
            
            # Wait for ready
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
            
            # Generate and show sequence
            show_sequence_with_tapping(screen, letters, trial_num, condition, length)
            
            # Brief pause before recall
            screen.fill(WHITE)
            pause_text = font_medium.render("Now recall the letters in order!", True, BLACK)
            pause_rect = pause_text.get_rect(center=(400, 300))
            screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            time.sleep(1)
            
            # Get recall
            recalled_letters = get_serial_recall_input(screen, participant_name, length, trial_num, condition)
            
            # Analyze trial
            analysis = analyze_tapping_effect(recalled_letters, letters)
            
            # Store trial data
            trial_data = {
                'trial_number': trial_num,
                'condition': condition,
                'sequence_length': length,
                'original_letters': letters,
                'recalled_letters': recalled_letters,
                'analysis': analysis
            }
            results[condition].append(trial_data)
            
            trial_num += 1
        
        # Calculate average performance for each condition
        control_accuracies = [trial['analysis']['accuracy_rate'] for trial in results['control']]
        tapping_accuracies = [trial['analysis']['accuracy_rate'] for trial in results['tapping']]
        
        avg_tapping_analysis = {
            'control_accuracy': sum(control_accuracies) / len(control_accuracies),
            'tapping_accuracy': sum(tapping_accuracies) / len(tapping_accuracies),
            'accuracy_effect': (sum(control_accuracies) / len(control_accuracies)) - (sum(tapping_accuracies) / len(tapping_accuracies)),
            'control_span': sum(trial['analysis']['correct_from_start'] for trial in results['control']) / len(results['control']),
            'tapping_span': sum(trial['analysis']['correct_from_start'] for trial in results['tapping']) / len(results['tapping']),
            'span_effect': (sum(trial['analysis']['correct_from_start'] for trial in results['control']) / len(results['control'])) - sum(trial['analysis']['correct_from_start'] for trial in results['tapping']) / len(results['tapping']),
            'total_control_trials': len(results['control']),
            'total_tapping_trials': len(results['tapping'])
        }
        
        # Show final results
        show_final_results(screen, participant_name, avg_tapping_analysis, results['control'] + results['tapping'])
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'finger_tapping',
            'all_trials': results['control'] + results['tapping'],
            'control_trials': results['control'],
            'tapping_trials': results['tapping'],
            'tapping_analysis': avg_tapping_analysis,
            'trials_per_condition': trials_per_condition,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed finger tapping test for {participant_name}")
        print(f"Tapping effect: {tapping_analysis['accuracy_effect']*100:+.1f}% accuracy, {tapping_analysis['span_effect']:+.1f} span")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()