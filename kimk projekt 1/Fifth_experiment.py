import pygame
import time
import json
from datetime import datetime
import random
import string

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 5: Working Memory Capacity")
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
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'  # Exclude vowels to avoid words
    return [random.choice(consonants) for _ in range(length)]

def show_sequence(screen, letters, trial_num, sequence_length):
    """Show the consonant sequence"""
    print(f"Starting sequence of length {sequence_length} (trial {trial_num})...")
    
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show trial info
        trial_text = font_small.render(f"Trial {trial_num} - Length {sequence_length}", True, BLUE)
        screen.blit(trial_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)  # 1 second per letter
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_serial_recall_input(screen, participant_name, sequence_length, trial_num):
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
                            
                            # Check if we have enough letters
                            if len(recalled_letters) >= sequence_length:
                                input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if current_input:
                        current_input = current_input[:-1]
                    elif recalled_letters:
                        # Backspace removes last entered letter
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
        
        title = font_medium.render(f"Serial Recall - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        trial_info = font_small.render(f"Trial {trial_num} - Enter {sequence_length} letters in EXACT order", True, BLACK)
        trial_rect = trial_info.get_rect(center=(400, 130))
        screen.blit(trial_info, trial_rect)
        
        instruction1 = font_small.render("Type each letter and press ENTER or SPACE", True, GRAY)
        instruction1_rect = instruction1.get_rect(center=(400, 160))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Backspace to remove letters", True, GRAY)
        instruction2_rect = instruction2.get_rect(center=(400, 185))
        screen.blit(instruction2, instruction2_rect)
        
        # Current input
        input_label = font_small.render(f"Position {len(recalled_letters) + 1}:", True, BLACK)
        screen.blit(input_label, (250, 250))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        input_rect = input_surface.get_rect(center=(400, 300))
        screen.blit(input_surface, input_rect)
        
        # Show sequence entered so far
        sequence_label = font_small.render(f"Sequence entered ({len(recalled_letters)}/{sequence_length}):", True, BLACK)
        screen.blit(sequence_label, (50, 380))
        
        # Display letters in sequence
        x_start = 50
        y_start = 420
        
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

def analyze_serial_recall(recalled_letters, original_letters):
    """Analyze serial recall performance"""
    
    # Perfect sequence match
    perfect_match = recalled_letters == original_letters
    
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
        'perfect_match': perfect_match,
        'correct_positions': correct_positions,
        'total_positions': len(original_letters),
        'position_accuracy': position_accuracy,
        'accuracy_rate': correct_positions / len(original_letters),
        'correct_from_start': correct_from_start
    }
    
    return results

def show_trial_results(screen, participant_name, analysis, trial_num, sequence_length):
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
        
        # Trial summary
        y_pos = 120
        if analysis['perfect_match']:
            summary = font_medium.render("✓ PERFECT RECALL!", True, GREEN)
        else:
            summary = font_medium.render(f"Score: {analysis['correct_positions']}/{analysis['total_positions']} positions correct", True, BLACK)
        
        summary_rect = summary.get_rect(center=(400, y_pos))
        screen.blit(summary, summary_rect)
        
        # Show sequences
        y_pos = 180
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
        
        # Stats
        y_pos += 80
        stats = [
            f"Correct from start: {analysis['correct_from_start']} letters",
            f"Position accuracy: {analysis['accuracy_rate']*100:.1f}%"
        ]
        
        for stat in stats:
            text = font_small.render(stat, True, BLACK)
            screen.blit(text, (50, y_pos))
            y_pos += 25
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def calculate_working_memory_performance(all_trials):
    """Calculate working memory performance across all 7-letter trials"""
    
    total_trials = len(all_trials)
    perfect_recalls = sum(1 for trial in all_trials if trial['analysis']['accuracy_rate'] == 1.0)
    
    # Calculate average performance metrics
    avg_accuracy = sum(trial['analysis']['accuracy_rate'] for trial in all_trials) / total_trials
    avg_correct_from_start = sum(trial['analysis']['correct_from_start'] for trial in all_trials) / total_trials
    avg_correct_positions = sum(trial['analysis']['correct_positions'] for trial in all_trials) / total_trials
    
    # Calculate distribution of performance
    performance_distribution = {
        '7_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 7),
        '6_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 6),
        '5_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 5),
        '4_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 4),
        '3_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 3),
        '2_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 2),
        '1_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 1),
        '0_correct': sum(1 for trial in all_trials if trial['analysis']['correct_positions'] == 0)
    }
    
    # Find best and worst performance
    best_trial = max(all_trials, key=lambda t: t['analysis']['correct_positions'])
    worst_trial = min(all_trials, key=lambda t: t['analysis']['correct_positions'])
    
    results = {
        'total_trials': total_trials,
        'perfect_recalls': perfect_recalls,
        'avg_accuracy': avg_accuracy,
        'avg_correct_from_start': avg_correct_from_start,
        'avg_correct_positions': avg_correct_positions,
        'performance_distribution': performance_distribution,
        'best_performance': best_trial['analysis']['correct_positions'],
        'worst_performance': worst_trial['analysis']['correct_positions'],
        'best_trial_number': best_trial['trial_number'],
        'worst_trial_number': worst_trial['trial_number']
    }
    
    return results

def show_final_results(screen, participant_name, performance_analysis, all_trials):
    """Show final working memory performance results"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Working Memory Performance - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Main performance results
        y_pos = 120
        results_text = [
            f"Total trials completed: {performance_analysis['total_trials']}",
            f"Perfect recalls (7/7): {performance_analysis['perfect_recalls']} trials",
            f"Average letters correct: {performance_analysis['avg_correct_positions']:.1f}/7",
            f"Average accuracy: {performance_analysis['avg_accuracy']*100:.1f}%",
            f"Average sequential span: {performance_analysis['avg_correct_from_start']:.1f} letters"
        ]
        
        for text in results_text:
            text_surface = font_small.render(text, True, BLACK)
            screen.blit(text_surface, (50, y_pos))
            y_pos += 25
        
        # Performance distribution
        y_pos += 30
        distribution_title = font_small.render("Performance Distribution:", True, BLACK)
        screen.blit(distribution_title, (50, y_pos))
        
        y_pos += 25
        dist = performance_analysis['performance_distribution']
        distribution_items = [
            f"7 correct: {dist['7_correct']} trials",
            f"6 correct: {dist['6_correct']} trials", 
            f"5 correct: {dist['5_correct']} trials",
            f"4 correct: {dist['4_correct']} trials",
            f"3 or fewer: {dist['3_correct'] + dist['2_correct'] + dist['1_correct'] + dist['0_correct']} trials"
        ]
        
        for item in distribution_items:
            item_surface = font_small.render(item, True, BLACK)
            screen.blit(item_surface, (70, y_pos))
            y_pos += 20
        
        # Best and worst performance
        y_pos += 30
        best_text = font_small.render(f"Best performance: {performance_analysis['best_performance']}/7 (Trial {performance_analysis['best_trial_number']})", True, GREEN)
        screen.blit(best_text, (50, y_pos))
        
        y_pos += 25
        worst_text = font_small.render(f"Worst performance: {performance_analysis['worst_performance']}/7 (Trial {performance_analysis['worst_trial_number']})", True, RED)
        screen.blit(worst_text, (50, y_pos))
        
        # Interpretation
        y_pos += 50
        interpretation = font_small.render("Interpretation:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        avg_correct = performance_analysis['avg_correct_positions']
        if avg_correct >= 6:
            interp_text = "✓ Excellent working memory performance"
            interp_color = GREEN
        elif avg_correct >= 5:
            interp_text = "✓ Good working memory performance"
            interp_color = GREEN
        elif avg_correct >= 4:
            interp_text = "~ Average working memory performance"
            interp_color = BLUE
        else:
            interp_text = "⚠ Below average working memory performance"
            interp_color = RED
        
        interp_surface = font_small.render(interp_text, True, interp_color)
        screen.blit(interp_surface, (50, y_pos))
        
        y_pos += 25
        span_text = font_small.render(f"Sequential span: {performance_analysis['avg_correct_from_start']:.1f} (normal range: 5-9)", True, GRAY)
        screen.blit(span_text, (50, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment5_working_memory_capacity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 5: Working Memory Capacity", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instructions = [
            "This experiment measures your working memory capacity:",
            "",
            "• You'll see sequences of 7 consonants (no vowels)",
            "• Each letter shows for 1 second",
            "• After each sequence, type letters back in EXACT order",
            "• You'll do multiple trials with 7-letter sequences",
            "• We'll measure how many letters you can remember correctly",
            "",
            "Tips:",
            "• Focus and try to rehearse the letters mentally",
            "• Type back as many as you can remember in order",
            "• It's normal to not remember all 7 - do your best!",
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
        
        # Run multiple trials with same length (7 letters)
        all_trials = []
        sequence_length = 7  # Fixed length for all trials
        trials_per_participant = 20  # 20 trials of 7-letter sequences
        trial_num = 1
        
        for trial in range(trials_per_participant):
            # Show trial introduction
            screen.fill(WHITE)
            trial_intro = font_medium.render(f"Trial {trial_num}/20: {sequence_length} Letters", True, BLACK)
            trial_rect = trial_intro.get_rect(center=(400, 250))
            screen.blit(trial_intro, trial_rect)
            
            ready_text = font_small.render("Press any key when ready", True, BLUE)
            ready_rect = ready_text.get_rect(center=(400, 320))
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
            letters = generate_consonant_sequence(sequence_length)
            show_sequence(screen, letters, trial_num, sequence_length)
            
            # Brief pause before recall
            screen.fill(WHITE)
            pause_text = font_medium.render("Now enter the letters in order!", True, BLACK)
            pause_rect = pause_text.get_rect(center=(400, 300))
            screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            time.sleep(1)
            
            # Get recall
            recalled_letters = get_serial_recall_input(screen, participant_name, sequence_length, trial_num)
            
            # Analyze trial
            analysis = analyze_serial_recall(recalled_letters, letters)
            
            # Show trial results
            show_trial_results(screen, participant_name, analysis, trial_num, sequence_length)
            
            # Store trial data
            trial_data = {
                'trial_number': trial_num,
                'sequence_length': sequence_length,
                'original_letters': letters,
                'recalled_letters': recalled_letters,
                'analysis': analysis
            }
            all_trials.append(trial_data)
            
            trial_num += 1
        
        # Calculate overall working memory performance
        capacity_analysis = calculate_working_memory_performance(all_trials)
        
        # Show final results
        show_final_results(screen, participant_name, capacity_analysis, all_trials)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'working_memory_capacity',
            'all_trials': all_trials,
            'capacity_analysis': capacity_analysis,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed working memory capacity test for {participant_name}")
        print(f"Estimated capacity: {capacity_analysis['estimated_capacity']} items")
        print(f"Longest perfect: {capacity_analysis['max_perfect_length']} items")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()