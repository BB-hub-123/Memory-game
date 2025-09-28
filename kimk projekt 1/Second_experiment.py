import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 2: Effect of Presentation Speed")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Two different letter sequences will be generated randomly for each trial
def generate_consonant_sequence(length=20):
    """Generate a random sequence of consonants (no vowels to avoid chunks)"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'  # Exclude vowels A, E, I, O, U
    return [random.choice(consonants) for _ in range(length)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
GRAY = (150, 150, 150)

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

def show_sequence(screen, letters, speed_type, presentation_time):
    """Show the letter sequence at specified speed"""
    print(f"Starting {speed_type} sequence ({presentation_time}s per letter)...")
    
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show speed indicator
        speed_text = font_small.render(f"{speed_type.upper()} CONDITION", True, BLUE)
        screen.blit(speed_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(presentation_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_free_recall_input(screen, participant_name, condition):
    """Get free recall input from participant"""
    recalled_letters = []
    current_input = ""
    time_limit = 120  # 2 minutes to recall
    start_time = time.time()
    
    input_active = True
    while input_active:
        current_time = time.time()
        elapsed = current_time - start_time
        remaining = max(0, time_limit - elapsed)
        
        if remaining <= 0:
            input_active = False
            continue
        
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
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_SPACE:
                    if current_input.strip():
                        letter = current_input.strip().upper()
                        if len(letter) == 1 and letter.isalpha():
                            recalled_letters.append(letter)
                        current_input = ""
                elif event.key == pygame.K_ESCAPE:
                    input_active = False
                elif len(current_input) < 1 and event.unicode.isalpha():
                    current_input = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Free Recall - {participant_name} ({condition})", True, BLACK)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        instruction1 = font_small.render("Type letters you remember (any order)", True, BLACK)
        instruction1_rect = instruction1.get_rect(center=(400, 130))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Press ENTER or SPACE after each letter", True, GRAY)
        instruction2_rect = instruction2.get_rect(center=(400, 160))
        screen.blit(instruction2, instruction2_rect)
        
        instruction3 = font_small.render("Press ESC when finished", True, BLUE)
        instruction3_rect = instruction3.get_rect(center=(400, 190))
        screen.blit(instruction3, instruction3_rect)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer_text = f"Time remaining: {minutes:02d}:{seconds:02d}"
        timer_surface = font_medium.render(timer_text, True, RED)
        timer_rect = timer_surface.get_rect(center=(400, 240))
        screen.blit(timer_surface, timer_rect)
        
        input_label = font_small.render("Current letter:", True, BLACK)
        screen.blit(input_label, (200, 300))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        input_rect = input_surface.get_rect(center=(400, 340))
        screen.blit(input_surface, input_rect)
        
        recall_label = font_small.render(f"Letters recalled ({len(recalled_letters)}):", True, BLACK)
        screen.blit(recall_label, (50, 400))
        
        letters_per_row = 15
        x_start = 50
        y_start = 430
        
        for i, letter in enumerate(recalled_letters):
            row = i // letters_per_row
            col = i % letters_per_row
            x = x_start + col * 35
            y = y_start + row * 30
            
            letter_surface = font_medium.render(letter, True, BLACK)
            screen.blit(letter_surface, (x, y))
        
        bar_width = 700
        bar_height = 15
        bar_x = 50
        bar_y = 550
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        progress = remaining / time_limit
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), bar_height))
        
        pygame.display.flip()
    
    return recalled_letters

def analyze_speed_effect(recalled_letters, original_sequence):
    """Analyze recall performance for speed comparison"""
    
    # Calculate basic metrics
    correct_recalls = [letter for letter in recalled_letters if letter in original_sequence]
    false_recalls = [letter for letter in recalled_letters if letter not in original_sequence]
    
    unique_correct = list(set(correct_recalls))
    unique_false = list(set(false_recalls))
    
    # Position analysis
    position_recalls = []
    for recalled_letter in recalled_letters:
        positions = [i for i, orig_letter in enumerate(original_sequence) if orig_letter == recalled_letter]
        for pos in positions:
            if pos not in [p['position'] for p in position_recalls]:
                position_recalls.append({
                    'letter': recalled_letter,
                    'position': pos,
                    'serial_position': pos + 1
                })
    
    # Position-based recall data
    position_data = []
    for i in range(len(original_sequence)):
        was_recalled = any(pr['position'] == i for pr in position_recalls)
        position_data.append({
            'position': i + 1,
            'letter': original_sequence[i],
            'recalled': was_recalled
        })
    
    # Calculate primacy and recency for speed comparison
    primacy_positions = position_data[:5]
    middle_positions = position_data[5:15]
    recency_positions = position_data[15:]
    
    primacy_score = sum(1 for p in primacy_positions if p['recalled']) / len(primacy_positions)
    middle_score = sum(1 for p in middle_positions if p['recalled']) / len(middle_positions)
    recency_score = sum(1 for p in recency_positions if p['recalled']) / len(recency_positions)
    
    results = {
        'total_recalled': len(recalled_letters),
        'correct_recalls': len(correct_recalls),
        'unique_correct': len(unique_correct),
        'false_recalls': len(false_recalls),
        'recall_rate': len(unique_correct) / len(original_sequence),
        'precision': len(unique_correct) / len(set(recalled_letters)) if recalled_letters else 0,
        'primacy_score': primacy_score,
        'middle_score': middle_score,
        'recency_score': recency_score,
        'position_data': position_data
    }
    
    return results

def show_condition_results(screen, participant_name, condition, analysis):
    """Show results for one condition"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Results: {condition} Condition - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        y_pos = 120
        metrics = [
            f"Total letters recalled: {analysis['total_recalled']}",
            f"Correct letters: {analysis['unique_correct']}/20 ({analysis['recall_rate']*100:.1f}%)",
            f"False recalls: {analysis['false_recalls']}",
            f"Precision: {analysis['precision']*100:.1f}%",
            "",
            f"Primacy effect (1-5): {analysis['primacy_score']*100:.1f}%",
            f"Middle positions (6-15): {analysis['middle_score']*100:.1f}%",
            f"Recency effect (16-20): {analysis['recency_score']*100:.1f}%"
        ]
        
        for metric in metrics:
            if metric == "":
                y_pos += 10
                continue
            text = font_small.render(metric, True, BLACK)
            screen.blit(text, (50, y_pos))
            y_pos += 25
        
        # Serial position visualization
        y_pos += 20
        curve_label = font_small.render("Serial Position (✓ = recalled, ✗ = not recalled):", True, BLACK)
        screen.blit(curve_label, (50, y_pos))
        
        y_pos += 30
        for i, data in enumerate(analysis['position_data']):
            row = i // 10
            col = i % 10
            x = 50 + col * 70
            y = y_pos + row * 30
            
            symbol = "✓" if data['recalled'] else "✗"
            color = GREEN if data['recalled'] else RED
            
            pos_text = f"{data['position']}:{symbol}"
            pos_surface = font_small.render(pos_text, True, color)
            screen.blit(pos_surface, (x, y))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def show_comparison_results(screen, participant_name, slow_analysis, fast_analysis):
    """Show comparison between slow and fast conditions"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Speed Comparison - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Comparison table
        y_pos = 120
        headers = ["Metric", "Slow (1s/letter)", "Fast (0.5s/letter)", "Difference"]
        
        header_text = font_small.render(f"{headers[0]:<20} {headers[1]:<15} {headers[2]:<15} {headers[3]}", True, BLACK)
        screen.blit(header_text, (50, y_pos))
        y_pos += 30
        
        # Draw separator line
        pygame.draw.line(screen, BLACK, (50, y_pos), (750, y_pos), 2)
        y_pos += 20
        
        comparisons = [
            ("Total Recall", slow_analysis['recall_rate'], fast_analysis['recall_rate']),
            ("Primacy", slow_analysis['primacy_score'], fast_analysis['primacy_score']),
            ("Middle", slow_analysis['middle_score'], fast_analysis['middle_score']),
            ("Recency", slow_analysis['recency_score'], fast_analysis['recency_score']),
            ("Precision", slow_analysis['precision'], fast_analysis['precision'])
        ]
        
        for metric, slow_val, fast_val in comparisons:
            diff = slow_val - fast_val
            diff_symbol = "+" if diff > 0 else ""
            
            # Color code the difference
            if abs(diff) > 0.1:  # Substantial difference
                diff_color = GREEN if diff > 0 else RED
            else:
                diff_color = GRAY
            
            metric_text = font_small.render(f"{metric:<20}", True, BLACK)
            slow_text = font_small.render(f"{slow_val*100:>6.1f}%", True, BLACK)
            fast_text = font_small.render(f"{fast_val*100:>6.1f}%", True, BLACK)
            diff_text = font_small.render(f"{diff_symbol}{diff*100:>6.1f}%", True, diff_color)
            
            screen.blit(metric_text, (50, y_pos))
            screen.blit(slow_text, (250, y_pos))
            screen.blit(fast_text, (400, y_pos))
            screen.blit(diff_text, (550, y_pos))
            y_pos += 25
        
        # Speed effect interpretation
        y_pos += 30
        interpretation = font_small.render("Speed Effect Analysis:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        total_diff = slow_analysis['recall_rate'] - fast_analysis['recall_rate']
        if total_diff > 0.05:
            effect_text = "✓ Slower presentation improved overall recall"
            effect_color = GREEN
        elif total_diff < -0.05:
            effect_text = "⚠ Faster presentation improved overall recall (unexpected!)"
            effect_color = RED
        else:
            effect_text = "~ No significant speed effect on overall recall"
            effect_color = GRAY
        
        effect_surface = font_small.render(effect_text, True, effect_color)
        screen.blit(effect_surface, (50, y_pos))
        
        y_pos += 25
        primacy_diff = slow_analysis['primacy_score'] - fast_analysis['primacy_score']
        recency_diff = slow_analysis['recency_score'] - fast_analysis['recency_score']
        
        if primacy_diff > 0.1:
            primacy_text = "✓ Speed particularly affected primacy (early items)"
            screen.blit(font_small.render(primacy_text, True, GREEN), (50, y_pos))
            y_pos += 25
        
        if recency_diff > 0.1:
            recency_text = "✓ Speed particularly affected recency (late items)"
            screen.blit(font_small.render(recency_text, True, GREEN), (50, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment2_presentation_speed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 2: Effect of Presentation Speed", True, BLACK)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        instructions = [
            "You will complete MULTIPLE memory tests:",
            "• Each test has 20 random consonant letters",
            "• SLOW condition: Letters shown for 1 second each",
            "• FAST condition: Letters shown for 0.5 seconds each",
            "• You'll do multiple trials of each condition",
            "",
            "For each test:",
            "- 20 different random letters will be shown",
            "- After each sequence, recall as many as possible",
            "- We'll compare how speed affects your memory",
            "",
            "Press any key to start"
        ]
        
        y_pos = 140
        for instruction in instructions:
            color = BLUE if instruction.startswith("Press") else BLACK
            if instruction == "":
                y_pos += 10
                continue
            text = font_small.render(instruction, True, color)
            screen.blit(text, (50, y_pos))
            y_pos += 25
        
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
        
        # Run multiple trials for each condition
        trials_per_condition = 10  # 10 trials each of slow and fast
        conditions = ['slow', 'fast']
        all_trials = []
        
        # Create trial list
        trial_list = []
        for condition in conditions:
            for trial in range(trials_per_condition):
                trial_list.append(condition)
        
        # Randomize order
        random.shuffle(trial_list)
        
        results = {'slow': [], 'fast': []}
        trial_num = 1
        
        for condition in trial_list:
            timing = 1.0 if condition == 'slow' else 0.5
            
            # Generate new random sequence for each trial
            letters = generate_consonant_sequence(20)
            
            # Show condition introduction
            screen.fill(WHITE)
            condition_title = font_medium.render(f"Trial {trial_num}/20: {condition.upper()} Presentation", True, BLACK)
            condition_rect = condition_title.get_rect(center=(400, 200))
            screen.blit(condition_title, condition_rect)
            
            timing_text = font_small.render(f"Each letter will be shown for {timing} seconds", True, BLUE)
            timing_rect = timing_text.get_rect(center=(400, 250))
            screen.blit(timing_text, timing_rect)
            
            ready_text = font_small.render("Press any key when ready", True, BLACK)
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
            
            # Countdown
            for count in [3, 2, 1]:
                screen.fill(WHITE)
                countdown = font_large.render(str(count), True, BLACK)
                countdown_rect = countdown.get_rect(center=(400, 300))
                screen.blit(countdown, countdown_rect)
                pygame.display.flip()
                time.sleep(1)
            
            # Show sequence
            show_sequence(screen, letters, condition, timing)
            
            # Brief pause
            screen.fill(WHITE)
            pause_text = font_medium.render(f"Now recall letters from trial {trial_num}!", True, BLACK)
            pause_rect = pause_text.get_rect(center=(400, 300))
            screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            time.sleep(2)
            
            # Get recall
            recalled_letters = get_free_recall_input(screen, participant_name, condition)
            
            # Analyze results
            analysis = analyze_speed_effect(recalled_letters, letters)
            
            # Store trial results
            trial_result = {
                'trial_number': trial_num,
                'condition': condition,
                'letters': letters,
                'recalled': recalled_letters,
                'analysis': analysis,
                'timing': timing
            }
            results[condition].append(trial_result)
            all_trials.append(trial_result)
            
            trial_num += 1
        
        # Calculate average performance for each condition
        slow_accuracies = [trial['analysis']['recall_rate'] for trial in results['slow']]
        fast_accuracies = [trial['analysis']['recall_rate'] for trial in results['fast']]
        
        avg_slow_analysis = {
            'recall_rate': sum(slow_accuracies) / len(slow_accuracies),
            'primacy_score': sum(trial['analysis']['primacy_score'] for trial in results['slow']) / len(results['slow']),
            'middle_score': sum(trial['analysis']['middle_score'] for trial in results['slow']) / len(results['slow']),
            'recency_score': sum(trial['analysis']['recency_score'] for trial in results['slow']) / len(results['slow'])
        }
        
        avg_fast_analysis = {
            'recall_rate': sum(fast_accuracies) / len(fast_accuracies),
            'primacy_score': sum(trial['analysis']['primacy_score'] for trial in results['fast']) / len(results['fast']),
            'middle_score': sum(trial['analysis']['middle_score'] for trial in results['fast']) / len(results['fast']),
            'recency_score': sum(trial['analysis']['recency_score'] for trial in results['fast']) / len(results['fast'])
        }
        
        # Show comparison
        show_comparison_results(screen, participant_name, avg_slow_analysis, avg_fast_analysis)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'presentation_speed_effect',
            'all_trials': all_trials,
            'slow_trials': results['slow'],
            'fast_trials': results['fast'],
            'avg_slow_analysis': avg_slow_analysis,
            'avg_fast_analysis': avg_fast_analysis,
            'trials_per_condition': trials_per_condition,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed speed comparison for {participant_name}")
        slow_rate = results['slow']['analysis']['recall_rate']
        fast_rate = results['fast']['analysis']['recall_rate']
        print(f"Slow: {slow_rate*100:.1f}%, Fast: {fast_rate*100:.1f}%, Difference: {(slow_rate-fast_rate)*100:+.1f}%")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()