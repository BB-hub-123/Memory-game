import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 7: Articulatory Suppression")
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

def show_sequence_with_suppression(screen, letters, trial_num, condition, sequence_length):
    """Show sequence with or without articulatory suppression"""
    print(f"Starting {condition} sequence of length {sequence_length} (trial {trial_num})...")
    
    suppression_active = (condition == "suppression")
    
    if suppression_active:
        # Show suppression instructions
        screen.fill(WHITE)
        suppression_title = font_medium.render("ARTICULATORY SUPPRESSION", True, RED)
        suppression_rect = suppression_title.get_rect(center=(400, 150))
        screen.blit(suppression_title, suppression_rect)
        
        instruction1 = font_small.render("Say 'ta-ta-ta-ta...' OUT LOUD", True, BLACK)
        instruction1_rect = instruction1.get_rect(center=(400, 200))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Keep saying 'ta-ta-ta' during the entire sequence", True, BLACK)
        instruction2_rect = instruction2.get_rect(center=(400, 230))
        screen.blit(instruction2, instruction2_rect)
        
        instruction3 = font_small.render("This blocks inner speech rehearsal", True, GRAY)
        instruction3_rect = instruction3.get_rect(center=(400, 280))
        screen.blit(instruction3, instruction3_rect)
        
        ready_text = font_small.render("Start saying 'ta-ta-ta' and press any key", True, BLUE)
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
        if suppression_active:
            condition_text = font_small.render("KEEP SAYING 'TA-TA-TA' OUT LOUD", True, RED)
            screen.blit(condition_text, (20, 20))
        else:
            condition_text = font_small.render(f"CONTROL - Trial {trial_num}", True, BLUE)
            screen.blit(condition_text, (20, 20))
        
        # Show sequence progress
        progress_text = font_small.render(f"Letter {i+1}/{sequence_length}", True, GRAY)
        screen.blit(progress_text, (20, 50))
        
        # Show the letter
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        # Reminder for suppression condition
        if suppression_active:
            reminder = font_medium.render("'ta-ta-ta-ta-ta'", True, RED)
            reminder_rect = reminder.get_rect(center=(400, 450))
            screen.blit(reminder, reminder_rect)
        
        pygame.display.flip()
        time.sleep(1)  # 1 second per letter
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    # Stop suppression reminder
    if suppression_active:
        screen.fill(WHITE)
        stop_text = font_medium.render("STOP saying 'ta-ta-ta'", True, GREEN)
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
        
        # Emphasize that suppression should stop during recall
        if condition == "suppression":
            emphasis = font_small.render("(Do NOT say 'ta-ta-ta' during recall)", True, RED)
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

def analyze_suppression_effect(recalled_letters, original_letters):
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

def analyze_articulatory_suppression_experiment(all_trials):
    """Analyze overall articulatory suppression effect"""
    
    control_trials = [t for t in all_trials if t['condition'] == 'control']
    suppression_trials = [t for t in all_trials if t['condition'] == 'suppression']
    
    # Calculate average performance by condition
    control_accuracy = sum(t['analysis']['accuracy_rate'] for t in control_trials) / len(control_trials) if control_trials else 0
    suppression_accuracy = sum(t['analysis']['accuracy_rate'] for t in suppression_trials) / len(suppression_trials) if suppression_trials else 0
    
    # Calculate average span (correct from start) by condition
    control_span = sum(t['analysis']['correct_from_start'] for t in control_trials) / len(control_trials) if control_trials else 0
    suppression_span = sum(t['analysis']['correct_from_start'] for t in suppression_trials) / len(suppression_trials) if suppression_trials else 0
    
    # Calculate suppression effect
    accuracy_effect = control_accuracy - suppression_accuracy
    span_effect = control_span - suppression_span
    
    # Performance by sequence length
    length_performance = {'control': {}, 'suppression': {}}
    
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
        'suppression_accuracy': suppression_accuracy,
        'accuracy_effect': accuracy_effect,
        'control_span': control_span,
        'suppression_span': suppression_span,
        'span_effect': span_effect,
        'length_performance': length_performance,
        'total_control_trials': len(control_trials),
        'total_suppression_trials': len(suppression_trials)
    }
    
    return results

def show_final_results(screen, participant_name, suppression_analysis, all_trials):
    """Show final articulatory suppression results"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Articulatory Suppression Results - {participant_name}", True, BLACK)
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
        control_text = f"Control      {suppression_analysis['control_accuracy']*100:>6.1f}%   {suppression_analysis['control_span']:>6.1f}     --"
        control_surface = font_small.render(control_text, True, BLACK)
        screen.blit(control_surface, (50, y_pos))
        
        y_pos += 20
        
        # Suppression condition
        suppress_text = f"Suppression  {suppression_analysis['suppression_accuracy']*100:>6.1f}%   {suppression_analysis['suppression_span']:>6.1f}   {suppression_analysis['accuracy_effect']*100:>+5.1f}%"
        suppress_surface = font_small.render(suppress_text, True, BLACK)
        screen.blit(suppress_surface, (50, y_pos))
        
        # Effect interpretation
        y_pos += 50
        interpretation = font_small.render("Articulatory Suppression Effect:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        if suppression_analysis['accuracy_effect'] > 0.1:
            effect_text = "✓ Strong suppression effect - rehearsal is important!"
            effect_color = RED
        elif suppression_analysis['accuracy_effect'] > 0.05:
            effect_text = "~ Moderate suppression effect"
            effect_color = BLUE
        else:
            effect_text = "✗ No clear suppression effect"
            effect_color = GRAY
        
        effect_surface = font_small.render(effect_text, True, effect_color)
        screen.blit(effect_surface, (50, y_pos))
        
        y_pos += 25
        if suppression_analysis['span_effect'] > 0.5:
            span_text = "✓ Span particularly affected by suppression"
            span_color = RED
        else:
            span_text = "~ Small effect on memory span"
            span_color = GRAY
        
        span_surface = font_small.render(span_text, True, span_color)
        screen.blit(span_surface, (50, y_pos))
        
        # Performance by length (if enough data)
        if len(suppression_analysis['length_performance']['control']) > 1:
            y_pos += 50
            length_header = font_small.render("Performance by Sequence Length:", True, BLACK)
            screen.blit(length_header, (50, y_pos))
            
            y_pos += 25
            for length in sorted(suppression_analysis['length_performance']['control'].keys()):
                if length in suppression_analysis['length_performance']['suppression']:
                    control_perf = suppression_analysis['length_performance']['control'][length]
                    suppress_perf = suppression_analysis['length_performance']['suppression'][length]
                    diff = control_perf - suppress_perf
                    
                    length_text = f"Length {length}: Control {control_perf*100:.1f}% vs Suppression {suppress_perf*100:.1f}% (Δ{diff*100:+.1f}%)"
                    color = RED if diff > 0.1 else GRAY
                    
                    length_surface = font_small.render(length_text, True, color)
                    screen.blit(length_surface, (50, y_pos))
                    y_pos += 20
        
        # Theory explanation
        y_pos += 30
        theory_label = font_small.render("Theory:", True, BLACK)
        screen.blit(theory_label, (50, y_pos))
        
        y_pos += 25
        theory_text = [
            "Articulatory suppression blocks the phonological loop",
            "Saying 'ta-ta-ta' prevents inner speech rehearsal",
            "Should reduce memory span by disrupting verbal working memory"
        ]
        
        for text in theory_text:
            theory_surface = font_small.render(text, True, GRAY)
            screen.blit(theory_surface, (50, y_pos))
            y_pos += 20
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment7_articulatory_suppression_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 7: Articulatory Suppression", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instructions = [
            "This experiment tests how blocking inner speech affects memory:",
            "",
            "You'll complete MULTIPLE trials with TWO types:",
            "",
            "CONTROL trials:",
            "• See random consonant sequences normally",
            "• Use any memory strategy you want",
            "",
            "SUPPRESSION trials:", 
            "• Say 'ta-ta-ta-ta' OUT LOUD during letter presentation",
            "• This blocks your inner speech rehearsal",
            "• Stop saying 'ta-ta-ta' when letters finish",
            "",
            "You'll do 20 trials total (10 of each type) with random sequences.",
            "Theory: Articulatory suppression should reduce memory span",
            "by preventing phonological rehearsal in working memory",
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
        trials_per_condition = 10  # 10 control + 10 suppression = 20 total
        conditions = ['control', 'suppression']
        
        # Create trial list
        trial_list = []
        for condition in conditions:
            for trial in range(trials_per_condition):
                trial_list.append(condition)
        
        # Randomize order
        random.shuffle(trial_list)
        
        results = {'control': [], 'suppression': []}
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
            
            if condition == "suppression":
                reminder = font_small.render("Remember: Say 'ta-ta-ta' OUT LOUD during letters", True, RED)
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
            show_sequence_with_suppression(screen, letters, trial_num, condition, length)
            
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
            analysis = analyze_suppression_effect(recalled_letters, letters)
            
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
        suppression_accuracies = [trial['analysis']['accuracy_rate'] for trial in results['suppression']]
        
        avg_suppression_analysis = {
            'control_accuracy': sum(control_accuracies) / len(control_accuracies),
            'suppression_accuracy': sum(suppression_accuracies) / len(suppression_accuracies),
            'accuracy_effect': (sum(control_accuracies) / len(control_accuracies)) - (sum(suppression_accuracies) / len(suppression_accuracies)),
            'control_span': sum(trial['analysis']['correct_from_start'] for trial in results['control']) / len(results['control']),
            'suppression_span': sum(trial['analysis']['correct_from_start'] for trial in results['suppression']) / len(results['suppression']),
            'span_effect': (sum(trial['analysis']['correct_from_start'] for trial in results['control']) / len(results['control'])) - (sum(trial['analysis']['correct_from_start'] for trial in results['suppression']) / len(results['suppression'])),
            'total_control_trials': len(results['control']),
            'total_suppression_trials': len(results['suppression'])
        }
        
        # Show final results
        show_final_results(screen, participant_name, avg_suppression_analysis, results['control'] + results['suppression'])
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'articulatory_suppression',
            'all_trials': results['control'] + results['suppression'],
            'control_trials': results['control'],
            'suppression_trials': results['suppression'],
            'suppression_analysis': avg_suppression_analysis,
            'trials_per_condition': trials_per_condition,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed articulatory suppression test for {participant_name}")
        print(f"Suppression effect: {suppression_analysis['accuracy_effect']*100:+.1f}% accuracy, {suppression_analysis['span_effect']:+.1f} span")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()