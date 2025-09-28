import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 3: Working Memory Task After List")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Generate random consonant sequences for each trial
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

def show_sequence(screen, letters, condition):
    """Show the letter sequence"""
    print(f"Starting {condition} sequence...")
    
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show condition indicator
        condition_text = font_small.render(f"{condition.upper()} CONDITION", True, BLUE)
        screen.blit(condition_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def digit_span_task(screen, participant_name, duration=20):
    """Simplified working memory distraction task - counting backwards"""
    print("Starting counting distraction task...")
    
    start_time = time.time()
    
    # Show instructions
    screen.fill(WHITE)
    title = font_medium.render("Distraction Task", True, BLACK)
    title_rect = title.get_rect(center=(400, 150))
    screen.blit(title, title_rect)
    
    instruction1 = font_small.render("Count backwards from 100 by 3s", True, BLACK)
    instruction1_rect = instruction1.get_rect(center=(400, 200))
    screen.blit(instruction1, instruction1_rect)
    
    instruction2 = font_small.render("Example: 100, 97, 94, 91, 88...", True, GRAY)
    instruction2_rect = instruction2.get_rect(center=(400, 230))
    screen.blit(instruction2, instruction2_rect)
    
    instruction3 = font_small.render("Type each number and press ENTER", True, BLACK)
    instruction3_rect = instruction3.get_rect(center=(400, 280))
    screen.blit(instruction3, instruction3_rect)
    
    ready = font_small.render("Press any key to start counting", True, BLUE)
    ready_rect = ready.get_rect(center=(400, 350))
    screen.blit(ready, ready_rect)
    
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
    
    # Counting task
    expected_number = 100
    numbers_entered = []
    current_input = ""
    
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_input.strip().isdigit():
                        number = int(current_input.strip())
                        numbers_entered.append(number)
                        current_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.unicode.isdigit():
                    current_input += event.unicode
        
        # Update display
        screen.fill(WHITE)
        
        # Timer
        elapsed = time.time() - start_time
        remaining = max(0, duration - elapsed)
        timer_text = font_medium.render(f"Time remaining: {remaining:.0f}s", True, RED)
        timer_rect = timer_text.get_rect(center=(400, 100))
        screen.blit(timer_text, timer_rect)
        
        # Instructions
        instruction = font_small.render("Count backwards from 100 by 3s", True, BLACK)
        instruction_rect = instruction.get_rect(center=(400, 150))
        screen.blit(instruction, instruction_rect)
        
        # Current input
        input_label = font_small.render("Current number:", True, BLACK)
        screen.blit(input_label, (250, 250))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        input_rect = input_surface.get_rect(center=(400, 300))
        screen.blit(input_surface, input_rect)
        
        # Show last few numbers entered
        if numbers_entered:
            last_numbers = numbers_entered[-5:]  # Show last 5
            numbers_text = "Numbers entered: " + ", ".join(map(str, last_numbers))
            if len(numbers_entered) > 5:
                numbers_text += "..."
            
            numbers_surface = font_small.render(numbers_text, True, GRAY)
            screen.blit(numbers_surface, (50, 400))
        
        # Progress bar
        bar_width = 600
        bar_height = 15
        bar_x = 100
        bar_y = 500
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        progress = (duration - remaining) / duration
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), bar_height))
        
        pygame.display.flip()
        
        if remaining <= 0:
            break
    
    # Calculate performance
    correct_sequence = []
    num = 100
    while num > 0:
        correct_sequence.append(num)
        num -= 3
    
    # Check how many correct
    correct_count = 0
    for i, entered_num in enumerate(numbers_entered):
        if i < len(correct_sequence) and entered_num == correct_sequence[i]:
            correct_count += 1
        else:
            break  # Stop at first error
    
    # Show completion
    screen.fill(WHITE)
    completion_text = font_medium.render("Counting task complete!", True, GREEN)
    completion_rect = completion_text.get_rect(center=(400, 250))
    screen.blit(completion_text, completion_rect)
    
    if numbers_entered:
        score_text = font_small.render(f"You entered {len(numbers_entered)} numbers, {correct_count} correct in sequence", True, BLACK)
        score_rect = score_text.get_rect(center=(400, 300))
        screen.blit(score_text, score_rect)
    
    pygame.display.flip()
    time.sleep(2)
    
    return {
        'numbers_entered': len(numbers_entered),
        'correct_sequence': correct_count,
        'accuracy': correct_count / len(numbers_entered) if numbers_entered else 0
    }

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
        
        instruction1 = font_small.render("Type letters you remember from the letter sequence", True, BLACK)
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

def analyze_working_memory_effect(recalled_letters, original_sequence):
    """Analyze recall performance for working memory comparison"""
    
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
    
    # Calculate primacy and recency effects
    primacy_positions = position_data[:5]
    middle_positions = position_data[5:15]
    recency_positions = position_data[15:]
    
    primacy_score = sum(1 for p in primacy_positions if p['recalled']) / len(primacy_positions)
    middle_score = sum(1 for p in middle_positions if p['recalled']) / len(middle_positions)
    recency_score = sum(1 for p in recency_positions if p['recalled']) / len(recency_positions)
    
    # Additional metrics
    correct_recalls = [letter for letter in recalled_letters if letter in original_sequence]
    unique_correct = list(set(correct_recalls))
    
    results = {
        'total_recalled': len(recalled_letters),
        'unique_correct': len(unique_correct),
        'recall_rate': len(unique_correct) / len(original_sequence),
        'primacy_score': primacy_score,
        'middle_score': middle_score,
        'recency_score': recency_score,
        'position_data': position_data
    }
    
    return results

def show_comparison_results(screen, participant_name, control_analysis, distraction_analysis, distraction_performance):
    """Show comparison between control and distraction conditions"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Working Memory Effect - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 40))
        screen.blit(title, title_rect)
        
        # Distraction task performance
        if distraction_performance:
            distraction_text = font_small.render(f"Counting task: {distraction_performance['numbers_entered']} numbers, {distraction_performance['correct_sequence']} correct in sequence", True, GRAY)
            screen.blit(distraction_text, (50, 80))
        
        # Comparison table
        y_pos = 120
        headers = ["Metric", "Control", "Distraction", "Effect"]
        
        header_text = font_small.render(f"{headers[0]:<20} {headers[1]:<12} {headers[2]:<12} {headers[3]}", True, BLACK)
        screen.blit(header_text, (50, y_pos))
        y_pos += 30
        
        # Draw separator line
        pygame.draw.line(screen, BLACK, (50, y_pos), (750, y_pos), 2)
        y_pos += 20
        
        comparisons = [
            ("Total Recall", control_analysis['recall_rate'], distraction_analysis['recall_rate']),
            ("Primacy (1-5)", control_analysis['primacy_score'], distraction_analysis['primacy_score']),
            ("Middle (6-15)", control_analysis['middle_score'], distraction_analysis['middle_score']),
            ("Recency (16-20)", control_analysis['recency_score'], distraction_analysis['recency_score'])
        ]
        
        for metric, control_val, distraction_val in comparisons:
            diff = control_val - distraction_val
            
            # Color code the effect
            if diff > 0.1:  # Control better
                effect_color = RED
                effect_text = f"-{diff*100:.1f}%"
            elif diff < -0.1:  # Distraction better (unexpected)
                effect_color = GREEN
                effect_text = f"+{abs(diff)*100:.1f}%"
            else:
                effect_color = GRAY
                effect_text = f"{diff*100:+.1f}%"
            
            metric_text = font_small.render(f"{metric:<20}", True, BLACK)
            control_text = font_small.render(f"{control_val*100:>6.1f}%", True, BLACK)
            distraction_text = font_small.render(f"{distraction_val*100:>6.1f}%", True, BLACK)
            effect_surface = font_small.render(effect_text, True, effect_color)
            
            screen.blit(metric_text, (50, y_pos))
            screen.blit(control_text, (250, y_pos))
            screen.blit(distraction_text, (350, y_pos))
            screen.blit(effect_surface, (450, y_pos))
            y_pos += 25
        
        # Working memory effect interpretation
        y_pos += 30
        interpretation = font_small.render("Working Memory Effect Analysis:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        total_diff = control_analysis['recall_rate'] - distraction_analysis['recall_rate']
        if total_diff > 0.05:
            effect_text = "✓ Distraction task reduced overall recall"
            effect_color = RED
        elif total_diff < -0.05:
            effect_text = "⚠ Distraction task improved recall (unexpected!)"
            effect_color = GREEN
        else:
            effect_text = "~ No significant effect on overall recall"
            effect_color = GRAY
        
        effect_surface = font_small.render(effect_text, True, effect_color)
        screen.blit(effect_surface, (50, y_pos))
        
        y_pos += 25
        primacy_diff = control_analysis['primacy_score'] - distraction_analysis['primacy_score']
        recency_diff = control_analysis['recency_score'] - distraction_analysis['recency_score']
        
        if recency_diff > 0.1:
            recency_text = "✓ Distraction particularly affected recency (recent items)"
            screen.blit(font_small.render(recency_text, True, RED), (50, y_pos))
            y_pos += 25
        
        if primacy_diff > 0.1:
            primacy_text = "✓ Distraction also affected primacy (early items)"
            screen.blit(font_small.render(primacy_text, True, RED), (50, y_pos))
            y_pos += 25
        
        if recency_diff > primacy_diff + 0.1:
            theory_text = "Theory: Working memory blocks rehearsal → hurts recency more"
            screen.blit(font_small.render(theory_text, True, BLUE), (50, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment3_working_memory_task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 3: Working Memory Task After List", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instructions = [
            "You will complete MULTIPLE memory tests:",
            "",
            "CONTROL trials:",
            "   - See 20 random consonant letters → immediately recall them",
            "",
            "DISTRACTION trials:",
            "   - See 20 random consonant letters → do counting task → recall letters",
            "   - Counting task: Count backwards from 100 by 3s",
            "",
            "You'll do multiple trials of each condition to get reliable data.",
            "This tests whether working memory tasks block rehearsal",
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
        trials_per_condition = 10  # 10 trials each of control and distraction
        conditions = ['control', 'distraction']
        
        # Create trial list
        trial_list = []
        for condition in conditions:
            for trial in range(trials_per_condition):
                trial_list.append(condition)
        
        # Randomize order
        random.shuffle(trial_list)
        
        results = {'control': [], 'distraction': []}
        distraction_performances = []
        trial_num = 1
        
        for condition in trial_list:
            has_distraction = (condition == 'distraction')
            
            # Generate new random sequence for each trial
            letters = generate_consonant_sequence(20)
            
            # Show condition introduction
            screen.fill(WHITE)
            condition_title = font_medium.render(f"Trial {trial_num}/20: {condition.upper()}", True, BLACK)
            condition_rect = condition_title.get_rect(center=(400, 200))
            screen.blit(condition_title, condition_rect)
            
            if has_distraction:
                task_text = font_small.render("After letters: counting task, then recall", True, BLUE)
            else:
                task_text = font_small.render("After letters: immediate recall", True, BLUE)
            task_rect = task_text.get_rect(center=(400, 250))
            screen.blit(task_text, task_rect)
            
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
            show_sequence(screen, letters, condition)
            
            # Distraction task or immediate recall
            distraction_performance = None
            if has_distraction:
                screen.fill(WHITE)
                transition_text = font_medium.render("Now do the counting task!", True, BLACK)
                transition_rect = transition_text.get_rect(center=(400, 300))
                screen.blit(transition_text, transition_rect)
                pygame.display.flip()
                time.sleep(1)
                
                distraction_performance = digit_span_task(screen, participant_name, duration=20)
                distraction_performances.append(distraction_performance)
                
                screen.fill(WHITE)
                recall_prompt = font_medium.render("Now recall the LETTERS from before the counting task!", True, BLACK)
                recall_rect = recall_prompt.get_rect(center=(400, 300))
                screen.blit(recall_prompt, recall_rect)
                pygame.display.flip()
                time.sleep(2)
            else:
                screen.fill(WHITE)
                pause_text = font_medium.render("Now recall the letters!", True, BLACK)
                pause_rect = pause_text.get_rect(center=(400, 300))
                screen.blit(pause_text, pause_rect)
                pygame.display.flip()
                time.sleep(2)
            
            # Get recall
            recalled_letters = get_free_recall_input(screen, participant_name, condition)
            
            # Analyze results
            analysis = analyze_working_memory_effect(recalled_letters, letters)
            
            # Store trial results
            trial_result = {
                'trial_number': trial_num,
                'condition': condition,
                'letters': letters,
                'recalled': recalled_letters,
                'analysis': analysis,
                'had_distraction': has_distraction,
                'distraction_performance': distraction_performance
            }
            results[condition].append(trial_result)
            
            trial_num += 1
        
        # Calculate average performance for each condition
        control_accuracies = [trial['analysis']['recall_rate'] for trial in results['control']]
        distraction_accuracies = [trial['analysis']['recall_rate'] for trial in results['distraction']]
        
        avg_control_analysis = {
            'recall_rate': sum(control_accuracies) / len(control_accuracies),
            'primacy_score': sum(trial['analysis']['primacy_score'] for trial in results['control']) / len(results['control']),
            'middle_score': sum(trial['analysis']['middle_score'] for trial in results['control']) / len(results['control']),
            'recency_score': sum(trial['analysis']['recency_score'] for trial in results['control']) / len(results['control'])
        }
        
        avg_distraction_analysis = {
            'recall_rate': sum(distraction_accuracies) / len(distraction_accuracies),
            'primacy_score': sum(trial['analysis']['primacy_score'] for trial in results['distraction']) / len(results['distraction']),
            'middle_score': sum(trial['analysis']['middle_score'] for trial in results['distraction']) / len(results['distraction']),
            'recency_score': sum(trial['analysis']['recency_score'] for trial in results['distraction']) / len(results['distraction'])
        }
        
        # Average distraction performance
        avg_distraction_performance = None
        if distraction_performances:
            avg_distraction_performance = {
                'numbers_entered': sum(p['numbers_entered'] for p in distraction_performances) / len(distraction_performances),
                'correct_sequence': sum(p['correct_sequence'] for p in distraction_performances) / len(distraction_performances),
                'accuracy': sum(p['accuracy'] for p in distraction_performances) / len(distraction_performances)
            }
        
        # Show comparison
        show_comparison_results(screen, participant_name, 
                               avg_control_analysis, 
                               avg_distraction_analysis,
                               avg_distraction_performance)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'working_memory_task_after_list',
            'all_trials': results['control'] + results['distraction'],
            'control_trials': results['control'],
            'distraction_trials': results['distraction'],
            'avg_control_analysis': avg_control_analysis,
            'avg_distraction_analysis': avg_distraction_analysis,
            'avg_distraction_performance': avg_distraction_performance,
            'trials_per_condition': trials_per_condition,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed working memory test for {participant_name}")
        control_rate = results['control']['analysis']['recall_rate']
        distraction_rate = results['distraction']['analysis']['recall_rate']
        print(f"Control: {control_rate*100:.1f}%, Distraction: {distraction_rate*100:.1f}%, Effect: {(control_rate-distraction_rate)*100:+.1f}%")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()