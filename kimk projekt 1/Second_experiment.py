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

def generate_consonant_sequence(length=15):
    """Generate a random sequence of unique consonants (no vowels, no repeats)"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'  # Exclude vowels A, E, I, O, U
    return random.sample(consonants, length)

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

def show_sequence(screen, letters, speed_type, presentation_time, trial_num):
    """Show the letter sequence at specified speed"""
    print(f"Trial {trial_num}: {speed_type} sequence ({presentation_time}s per letter)...")
    
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show trial and speed indicator
        info_text = font_small.render(f"Trial {trial_num}/20 - {speed_type.upper()} - Letter {i+1}/15", True, BLUE)
        screen.blit(info_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(presentation_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_free_recall_input(screen, participant_name, condition, trial_num):
    """Get free recall input from participant"""
    recalled_letters = []
    current_input = ""
    time_limit = 90  # 1.5 minutes to recall
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
        
        title = font_medium.render(f"Trial {trial_num} Recall - {condition.upper()}", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instruction1 = font_small.render("Type letters you remember (any order)", True, BLACK)
        screen.blit(instruction1, (400 - instruction1.get_width()//2, 110))
        
        instruction2 = font_small.render("ENTER/SPACE after each | ESC when done", True, GRAY)
        screen.blit(instruction2, (400 - instruction2.get_width()//2, 140))
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        timer_surface = font_medium.render(timer_text, True, RED)
        screen.blit(timer_surface, (400 - timer_surface.get_width()//2, 190))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        screen.blit(input_surface, (400 - input_surface.get_width()//2, 260))
        
        recall_label = font_small.render(f"Recalled ({len(recalled_letters)}):", True, BLACK)
        screen.blit(recall_label, (50, 360))
        
        # Show recalled letters
        x, y = 50, 390
        for i, letter in enumerate(recalled_letters):
            if i > 0 and i % 15 == 0:
                y += 30
                x = 50
            letter_surface = font_medium.render(letter, True, BLACK)
            screen.blit(letter_surface, (x, y))
            x += 35
        
        # Progress bar
        bar_width = 700
        bar_x = 50
        bar_y = 550
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, 15))
        progress = remaining / time_limit
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), 15))
        
        pygame.display.flip()
    
    return recalled_letters

def analyze_speed_effect(recalled_letters, original_sequence):
    """Analyze recall performance"""
    sequence_length = len(original_sequence)
    
    # Calculate metrics
    correct_recalls = [letter for letter in recalled_letters if letter in original_sequence]
    unique_correct = list(set(correct_recalls))
    
    # Position analysis - which positions were recalled
    position_data = []
    for i, orig_letter in enumerate(original_sequence):
        was_recalled = orig_letter in recalled_letters
        position_data.append({
            'position': i + 1,
            'letter': orig_letter,
            'recalled': was_recalled
        })
    
    # Primacy, middle, recency (adjusted for 15 items)
    primacy_positions = position_data[:5]  # First 5
    middle_positions = position_data[5:10]  # Middle 5
    recency_positions = position_data[10:]  # Last 5
    
    primacy_score = sum(1 for p in primacy_positions if p['recalled']) / len(primacy_positions)
    middle_score = sum(1 for p in middle_positions if p['recalled']) / len(middle_positions)
    recency_score = sum(1 for p in recency_positions if p['recalled']) / len(recency_positions)
    
    results = {
        'total_recalled': len(recalled_letters),
        'unique_correct': len(unique_correct),
        'recall_rate': len(unique_correct) / sequence_length,
        'primacy_score': primacy_score,
        'middle_score': middle_score,
        'recency_score': recency_score,
        'position_data': position_data
    }
    
    return results

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"exp2_{all_results[0]['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"Data saved to {filename}")

def main():
    """Main experiment loop"""
    participant_name = get_text_input(screen, "Enter participant name:")
    
    if not participant_name:
        pygame.quit()
        return
    
    # Instructions
    screen.fill(WHITE)
    instructions = [
        "Experiment 2: Presentation Speed",
        "",
        "20 trials total (10 slow, 10 fast)",
        "",
        "SLOW: 1 second per letter",
        "FAST: 0.5 seconds per letter",
        "",
        "Each trial: 15 unique letters shown one at a time",
        "Then recall as many as you can (any order)",
        "",
        "Press any key to start"
    ]
    
    y = 140
    for line in instructions:
        color = BLUE if "Press" in line else BLACK
        text = font_small.render(line, True, color)
        screen.blit(text, (400 - text.get_width()//2, y))
        y += 35
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    # Create trial list (10 slow + 10 fast)
    trial_list = ['slow'] * 10 + ['fast'] * 10
    random.shuffle(trial_list)
    
    results = []
    
    # Run 20 trials
    for i, condition in enumerate(trial_list):
        trial_num = i + 1
        timing = 1.0 if condition == 'slow' else 0.5
        
        # Generate unique sequence
        letters = generate_consonant_sequence(15)
        
        # Ready screen
        screen.fill(WHITE)
        ready_title = font_medium.render(f"Trial {trial_num}/20: {condition.upper()}", True, BLACK)
        screen.blit(ready_title, (400 - ready_title.get_width()//2, 180))
        
        timing_text = font_small.render(f"{timing} seconds per letter", True, BLUE)
        screen.blit(timing_text, (400 - timing_text.get_width()//2, 240))
        
        instruction = font_small.render("Press any key when ready", True, BLACK)
        screen.blit(instruction, (400 - instruction.get_width()//2, 300))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        
        # Countdown
        for count in [3, 2, 1]:
            screen.fill(WHITE)
            countdown = font_large.render(str(count), True, BLACK)
            screen.blit(countdown, (400 - countdown.get_width()//2, 250))
            pygame.display.flip()
            time.sleep(1)
        
        # Show sequence
        show_sequence(screen, letters, condition, timing, trial_num)
        
        # Brief pause
        screen.fill(WHITE)
        pause_text = font_medium.render("Now recall the letters!", True, BLACK)
        screen.blit(pause_text, (400 - pause_text.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
        
        # Get recall
        recalled = get_free_recall_input(screen, participant_name, condition, trial_num)
        
        # Analyze
        analysis = analyze_speed_effect(recalled, letters)
        
        # Store results
        results.append({
            'trial': trial_num,
            'condition': condition,
            'timing': timing,
            'original': letters,
            'recalled': recalled,
            'unique_correct': analysis['unique_correct'],
            'recall_rate': analysis['recall_rate'],
            'primacy': analysis['primacy_score'],
            'middle': analysis['middle_score'],
            'recency': analysis['recency_score']
        })
        
        # Brief feedback
        screen.fill(WHITE)
        score = font_medium.render(f"Recalled: {analysis['unique_correct']}/15", True, BLACK)
        screen.blit(score, (400 - score.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    slow = [r for r in results if r['condition'] == 'slow']
    fast = [r for r in results if r['condition'] == 'fast']
    
    slow_acc = sum(t['recall_rate'] for t in slow) / len(slow) * 100
    fast_acc = sum(t['recall_rate'] for t in fast) / len(fast) * 100
    effect = slow_acc - fast_acc
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (400 - title.get_width()//2, 150))
    
    summary = [
        f"Slow (1s): {slow_acc:.1f}%",
        f"Fast (0.5s): {fast_acc:.1f}%",
        f"Difference: {effect:+.1f}%"
    ]
    
    y = 250
    for line in summary:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (400 - text.get_width()//2, y))
        y += 40
    
    if effect > 10:
        interpretation = "Slow presentation helped significantly!"
        color = GREEN
    elif effect > 5:
        interpretation = "Moderate speed effect"
        color = BLUE
    else:
        interpretation = "Minimal speed effect"
        color = GRAY
    
    interp_text = font_small.render(interpretation, True, color)
    screen.blit(interp_text, (400 - interp_text.get_width()//2, y + 30))
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save data
    data = [{
        'name': participant_name,
        'timestamp': datetime.now().isoformat(),
        'trials': results,
        'summary': {
            'slow_accuracy': slow_acc / 100,
            'fast_accuracy': fast_acc / 100,
            'speed_effect': effect / 100
        }
    }]
    save_data(data)
    
    pygame.quit()

if __name__ == "__main__":
    main()