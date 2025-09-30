import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 4: Delayed Memory")
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

def show_delay_period(screen, trial_num):
    """Show 20-second delay with countdown"""
    delay_time = 20
    
    for remaining in range(delay_time, 0, -1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Trial {trial_num}/20 - Delay Period", True, BLACK)
        screen.blit(title, (400 - title.get_width()//2, 120))
        
        instruction = font_small.render("Remember the letters you just saw", True, BLUE)
        screen.blit(instruction, (400 - instruction.get_width()//2, 180))
        
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        timer_surface = font_large.render(timer_text, True, RED)
        screen.blit(timer_surface, (400 - timer_surface.get_width()//2, 280))
        
        # Progress bar
        bar_width = 400
        bar_x = 200
        bar_y = 400
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, 20))
        
        progress_fill = (delay_time - remaining) / delay_time
        fill_width = int(bar_width * progress_fill)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, fill_width, 20))
        
        pygame.display.flip()
        time.sleep(1)

def get_serial_recall(screen, trial_num, sequence_length):
    """Get serial recall - one letter at a time in order"""
    recalled = []
    
    for position in range(sequence_length):
        current = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current.strip() and current.strip().isalpha():
                            recalled.append(current.strip().upper())
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        current = current[:-1]
                    elif len(current) < 1 and event.unicode.isalpha():
                        current = event.unicode.upper()
            
            screen.fill(WHITE)
            
            title = font_medium.render(f"Trial {trial_num}/20 - Recall", True, BLACK)
            screen.blit(title, (400 - title.get_width()//2, 80))
            
            prompt = font_small.render(f"Position {position + 1}/{sequence_length} - What letter?", True, BLACK)
            screen.blit(prompt, (400 - prompt.get_width()//2, 150))
            
            input_surface = font_large.render(current + "|", True, BLACK)
            screen.blit(input_surface, (400 - input_surface.get_width()//2, 250))
            
            instruction = font_small.render("Press ENTER to confirm", True, BLUE)
            screen.blit(instruction, (400 - instruction.get_width()//2, 380))
            
            # Show what's been recalled so far
            recalled_text = "Recalled: " + " ".join(recalled)
            recalled_surface = font_small.render(recalled_text, True, (100, 100, 100))
            screen.blit(recalled_surface, (50, 500))
            
            pygame.display.flip()
    
    return recalled

def analyze_trial(recalled, original):
    """Analyze trial results"""
    correct = sum(1 for i in range(len(original)) if i < len(recalled) and recalled[i] == original[i])
    return {
        'correct': correct,
        'accuracy': correct / len(original)
    }

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp4_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
        'delay_seconds': 20,
        'trials': trials,
        'summary': {
            'average_accuracy': sum(t['accuracy'] for t in trials) / len(trials),
            'total_trials': len(trials)
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to {filename}")

def main():
    """Main experiment"""
    participant_name = get_text_input(screen, "Enter participant name:")
    
    if not participant_name:
        pygame.quit()
        return
    
    # Instructions
    screen.fill(WHITE)
    instructions = [
        "Experiment 4: Delayed Memory",
        "",
        "20 trials with 20-second delay",
        "",
        "Each trial:",
        "1. See 15 letters (1 sec each)",
        "2. Wait 20 seconds (delay period)",
        "3. Recall letters in order",
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
        
        # 60-second delay
        show_delay_period(screen, trial_num)
        
        # Get recall
        recalled = get_serial_recall(screen, trial_num, 15)
        
        # Analyze
        analysis = analyze_trial(recalled, letters)
        
        # Store
        results.append({
            'trial': trial_num,
            'original': letters,
            'recalled': recalled,
            'correct': analysis['correct'],
            'accuracy': analysis['accuracy']
        })
        
        # Brief feedback
        screen.fill(WHITE)
        score = font_medium.render(f"Score: {analysis['correct']}/15", True, BLACK)
        screen.blit(score, (400 - score.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    avg_acc = sum(t['accuracy'] for t in results) / len(results) * 100
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (400 - title.get_width()//2, 200))
    
    summary = font_small.render(f"Average accuracy: {avg_acc:.1f}%", True, BLACK)
    screen.blit(summary, (400 - summary.get_width()//2, 280))
    
    note = font_small.render("(with 20-second delay)", True, BLUE)
    screen.blit(note, (400 - note.get_width()//2, 320))
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()