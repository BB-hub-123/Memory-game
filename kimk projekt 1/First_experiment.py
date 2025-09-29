import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 1: Primacy and Recency Effect")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

def generate_consonant_sequence(length=15):
    """Generate unique consonants (no vowels, no repeats)"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
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
        
        pygame.display.flip()
    
    return text.strip()

def show_sequence(screen, letters, trial_num):
    """Show the 15-letter sequence"""
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        # Show trial and position info
        info_text = font_small.render(f"Trial {trial_num}/20 - Letter {i+1}/15", True, BLUE)
        screen.blit(info_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_free_recall_input(screen, trial_num):
    """Get free recall input from participant"""
    recalled_letters = []
    current_input = ""
    time_limit = 90
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
                elif event.unicode and event.unicode.isalpha() and len(current_input) == 0:
                    current_input = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Trial {trial_num}/20 - Free Recall", True, BLACK)
        title_rect = title.get_rect(center=(400, 60))
        screen.blit(title, title_rect)
        
        instruction1 = font_small.render("Type letters you remember (any order)", True, BLACK)
        screen.blit(instruction1, (400 - instruction1.get_width()//2, 110))
        
        instruction2 = font_small.render("ENTER/SPACE after each | ESC when done", True, GRAY)
        screen.blit(instruction2, (400 - instruction2.get_width()//2, 140))
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"
        timer_surface = font_medium.render(timer_text, True, RED)
        screen.blit(timer_surface, (400 - timer_surface.get_width()//2, 190))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        screen.blit(input_surface, (400 - input_surface.get_width()//2, 260))
        
        recall_label = font_small.render(f"Recalled ({len(recalled_letters)}):", True, BLACK)
        screen.blit(recall_label, (50, 350))
        
        x, y = 50, 380
        for i, letter in enumerate(recalled_letters):
            if i > 0 and i % 15 == 0:
                y += 30
                x = 50
            letter_surface = font_medium.render(letter, True, BLACK)
            screen.blit(letter_surface, (x, y))
            x += 35
        
        bar_width = 700
        bar_x = 50
        bar_y = 550
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, 15))
        progress = remaining / time_limit
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), 15))
        
        pygame.display.flip()
    
    return recalled_letters

def analyze_primacy_recency(recalled_letters, original_sequence):
    """Analyze recall by serial position"""
    
    # Position mapping
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
    
    # Position data
    position_data = []
    for i in range(len(original_sequence)):
        was_recalled = any(pr['position'] == i for pr in position_recalls)
        position_data.append({
            'position': i + 1,
            'letter': original_sequence[i],
            'recalled': was_recalled
        })
    
    # Primacy, middle, recency (adjusted for 15 items)
    primacy_positions = position_data[:5]
    middle_positions = position_data[5:10]
    recency_positions = position_data[10:]
    
    primacy_score = sum(1 for p in primacy_positions if p['recalled']) / len(primacy_positions)
    middle_score = sum(1 for p in middle_positions if p['recalled']) / len(middle_positions)
    recency_score = sum(1 for p in recency_positions if p['recalled']) / len(recency_positions)
    
    results = {
        'position_data': position_data,
        'primacy_score': primacy_score,
        'middle_score': middle_score,
        'recency_score': recency_score,
        'total_recalled': len(position_recalls)
    }
    
    return results

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp1_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
        'trials': trials,
        'summary': {
            'average_primacy': sum(t['primacy_score'] for t in trials) / len(trials),
            'average_middle': sum(t['middle_score'] for t in trials) / len(trials),
            'average_recency': sum(t['recency_score'] for t in trials) / len(trials),
            'total_trials': len(trials)
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
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
        "Experiment 1: Primacy and Recency Effect",
        "",
        "20 trials - Control condition",
        "",
        "Each trial: 15 letters (1 sec each)",
        "Then recall as many as you can (any order)",
        "",
        "Tests memory for early (primacy) vs late (recency) items",
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
    
    results = []
    
    # Run 20 trials
    for trial_num in range(1, 21):
        # Generate NEW sequence for each trial
        letters = generate_consonant_sequence(15)
        
        # Ready screen
        screen.fill(WHITE)
        ready_title = font_medium.render(f"Trial {trial_num}/20", True, BLACK)
        screen.blit(ready_title, (400 - ready_title.get_width()//2, 240))
        
        instruction = font_small.render("Press any key when ready", True, BLUE)
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
        
        # Show sequence
        show_sequence(screen, letters, trial_num)
        
        # Get recall
        recalled = get_free_recall_input(screen, trial_num)
        
        # Analyze
        analysis = analyze_primacy_recency(recalled, letters)
        
        # Store
        results.append({
            'trial': trial_num,
            'original': letters,
            'recalled': recalled,
            'total_recalled': analysis['total_recalled'],
            'primacy_score': analysis['primacy_score'],
            'middle_score': analysis['middle_score'],
            'recency_score': analysis['recency_score']
        })
        
        # Brief feedback
        screen.fill(WHITE)
        score = font_medium.render(f"Recalled: {analysis['total_recalled']}/15", True, BLACK)
        screen.blit(score, (400 - score.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    avg_primacy = sum(t['primacy_score'] for t in results) / len(results) * 100
    avg_middle = sum(t['middle_score'] for t in results) / len(results) * 100
    avg_recency = sum(t['recency_score'] for t in results) / len(results) * 100
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (400 - title.get_width()//2, 150))
    
    summary = [
        f"Primacy (1-5): {avg_primacy:.1f}%",
        f"Middle (6-10): {avg_middle:.1f}%",
        f"Recency (11-15): {avg_recency:.1f}%"
    ]
    
    y = 240
    for line in summary:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (400 - text.get_width()//2, y))
        y += 35
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()