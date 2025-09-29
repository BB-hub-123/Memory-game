import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
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
        prompt_rect = prompt_surface.get_rect(center=(500, 250))
        screen.blit(prompt_surface, prompt_rect)
        
        text_surface = font_medium.render(text + "|", True, BLACK)
        text_rect = text_surface.get_rect(center=(500, 320))
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    return text.strip()

def generate_consonants(length=7):
    """Generate random consonants without repeats"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    return random.sample(consonants, length)

def show_letters(screen, letters, trial_num):
    """Show 7 letters one at a time with tapping"""
    
    # Show tapping instruction
    screen.fill(WHITE)
    title = font_medium.render("TAP YOUR FINGER ON DESK", True, BLUE)
    screen.blit(title, (500 - title.get_width()//2, 200))
    
    instruction = font_small.render("Keep tapping at steady rhythm during letters", True, BLACK)
    screen.blit(instruction, (500 - instruction.get_width()//2, 250))
    
    ready = font_small.render("Start tapping and press any key", True, BLUE)
    screen.blit(ready, (500 - ready.get_width()//2, 320))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    # Show letters
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        reminder = font_small.render("KEEP TAPPING", True, BLUE)
        screen.blit(reminder, (20, 20))
        
        trial_text = font_small.render(f"Trial {trial_num}/20 - Letter {i+1}/7", True, BLUE)
        screen.blit(trial_text, (20, 50))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(500, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    # Stop tapping
    screen.fill(WHITE)
    stop = font_medium.render("STOP tapping", True, GREEN)
    screen.blit(stop, (500 - stop.get_width()//2, 280))
    pygame.display.flip()
    time.sleep(1.5)

def get_recall(screen, trial_num):
    """Get 7 letters recall"""
    recalled = []
    current = ""
    
    while len(recalled) < 7:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if current.strip() and current.strip().isalpha():
                        recalled.append(current.strip().upper())
                        current = ""
                elif event.key == pygame.K_BACKSPACE:
                    if current:
                        current = current[:-1]
                    elif recalled:
                        recalled.pop()
                elif event.key == pygame.K_ESCAPE:
                    while len(recalled) < 7:
                        recalled.append("")
                    return recalled
                elif len(current) < 1 and event.unicode.isalpha():
                    current = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Trial {trial_num}/20 - Recall", True, BLACK)
        screen.blit(title, (500 - title.get_width()//2, 80))
        
        note = font_small.render("(Do NOT tap during recall)", True, BLUE)
        screen.blit(note, (500 - note.get_width()//2, 130))
        
        instruction = font_small.render("Type letters and press ENTER/SPACE", True, GRAY)
        screen.blit(instruction, (500 - instruction.get_width()//2, 160))
        
        # Current input
        input_surface = font_large.render(current + "|", True, BLACK)
        screen.blit(input_surface, (500 - input_surface.get_width()//2, 230))
        
        # Show recalled letters
        x_start = 200
        for i in range(7):
            x = x_start + i * 80
            color = GREEN if i < len(recalled) else GRAY
            pygame.draw.rect(screen, color, (x, 400, 70, 70), 3)
            
            if i < len(recalled):
                letter_surf = font_medium.render(recalled[i], True, BLACK)
                screen.blit(letter_surf, (x + 25, 415))
        
        pygame.display.flip()
    
    return recalled

def analyze_trial(recalled, original):
    """Analyze trial results"""
    correct = sum(1 for i in range(7) if i < len(recalled) and recalled[i] == original[i])
    return {
        'original': original,
        'recalled': recalled,
        'correct': correct,
        'accuracy': correct / 7
    }

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp8_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
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
        "Experiment 8: Finger Tapping",
        "",
        "20 trials with finger tapping",
        "",
        "Each trial:",
        "Tap finger on desk during letters",
        "Stop after letters, then recall in order",
        "",
        "7 letters per trial (1 sec each)",
        "",
        "Press any key to start"
    ]
    
    y = 120
    for line in instructions:
        color = BLUE if "Press" in line else BLACK
        text = font_small.render(line, True, color)
        screen.blit(text, (500 - text.get_width()//2, y))
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
    
    # Run 20 trials (all with tapping)
    for trial_num in range(1, 21):
        # Ready screen
        screen.fill(WHITE)
        ready_title = font_medium.render(f"Trial {trial_num}/20", True, BLACK)
        screen.blit(ready_title, (500 - ready_title.get_width()//2, 200))
        
        reminder = font_small.render("Remember: Tap finger on desk during letters", True, BLUE)
        screen.blit(reminder, (500 - reminder.get_width()//2, 260))
        
        instruction = font_small.render("Press any key when ready", True, BLUE)
        screen.blit(instruction, (500 - instruction.get_width()//2, 320))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        
        # Generate and show letters
        letters = generate_consonants(7)
        show_letters(screen, letters, trial_num)
        
        # Get recall
        recalled = get_recall(screen, trial_num)
        
        # Analyze
        analysis = analyze_trial(recalled, letters)
        
        # Store results
        results.append({
            'trial': trial_num,
            'original': letters,
            'recalled': recalled,
            'correct': analysis['correct'],
            'accuracy': analysis['accuracy']
        })
        
        # Brief feedback
        screen.fill(WHITE)
        score = font_medium.render(f"Score: {analysis['correct']}/7", True, BLACK)
        screen.blit(score, (500 - score.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    avg_acc = sum(t['accuracy'] for t in results) / len(results) * 100
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (500 - title.get_width()//2, 200))
    
    summary = font_small.render(f"Average accuracy: {avg_acc:.1f}%", True, BLACK)
    screen.blit(summary, (500 - summary.get_width()//2, 280))
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save data
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()