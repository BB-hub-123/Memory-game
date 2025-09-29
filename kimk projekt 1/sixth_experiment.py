import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Experiment 6: Chunking")
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

def generate_sequences():
    """Generate 10 chunkable and 10 random sequences with unique letters"""
    four_letter_words = [
        'HAND', 'DOOR', 'BOOK', 'TREE', 'FACE', 'BLUE', 'COLD', 'DARK',
        'FAST', 'GOOD', 'HARD', 'HIGH', 'LAST', 'LONG', 'MAKE', 'NICE',
        'OPEN', 'PLAY', 'ROAD', 'SAFE', 'SOFT', 'TALK', 'WARM', 'WILD'
    ]
    
    random_consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    sequences = []
    
    # 10 chunkable sequences (word + 3 random letters, all unique)
    for _ in range(10):
        word = random.choice(four_letter_words)
        word_letters = list(word)
        
        # Get 3 random letters that don't appear in the word
        available_consonants = [c for c in random_consonants if c not in word_letters]
        random_letters = random.sample(available_consonants, 3)
        
        position = random.choice(['start', 'end'])
        if position == 'start':
            sequence = word_letters + random_letters
        else:
            sequence = random_letters + word_letters
        
        sequences.append({
            'sequence': sequence,
            'type': 'chunkable',
            'word': word
        })
    
    # 10 random sequences (7 unique consonants)
    for _ in range(10):
        sequence = random.sample(random_consonants, 7)
        sequences.append({
            'sequence': sequence,
            'type': 'random',
            'word': None
        })
    
    random.shuffle(sequences)
    return sequences

def show_letters(screen, letters, trial_num):
    """Show 7 letters one at a time"""
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        trial_text = font_small.render(f"Trial {trial_num}/20 - Letter {i+1}/7", True, BLUE)
        screen.blit(trial_text, (20, 20))
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(500, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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
        
        instruction = font_small.render("Type letters and press ENTER/SPACE", True, GRAY)
        screen.blit(instruction, (500 - instruction.get_width()//2, 130))
        
        # Current input
        input_surface = font_large.render(current + "|", True, BLACK)
        screen.blit(input_surface, (500 - input_surface.get_width()//2, 200))
        
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

def analyze_trial(recalled, original_data):
    """Analyze trial results"""
    original = original_data['sequence']
    correct = sum(1 for i in range(7) if i < len(recalled) and recalled[i] == original[i])
    
    return {
        'original': original,
        'recalled': recalled,
        'correct': correct,
        'accuracy': correct / 7,
        'type': original_data['type'],
        'word': original_data['word']
    }

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp6_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    chunkable = [t for t in trials if t['type'] == 'chunkable']
    random_trials = [t for t in trials if t['type'] == 'random']
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
        'trials': trials,
        'summary': {
            'chunkable_accuracy': sum(t['accuracy'] for t in chunkable) / len(chunkable),
            'random_accuracy': sum(t['accuracy'] for t in random_trials) / len(random_trials),
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
        "Experiment 6: Chunking",
        "",
        "You will see 7 letters, one at a time (1 sec each)",
        "Then recall them in order",
        "20 trials total",
        "",
        "Press any key to start"
    ]
    
    y = 150
    for line in instructions:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (500 - text.get_width()//2, y))
        y += 40
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    # Generate sequences
    sequences = generate_sequences()
    results = []
    
    # Run 20 trials
    for i, seq_data in enumerate(sequences):
        trial_num = i + 1
        
        # Ready screen
        screen.fill(WHITE)
        ready = font_medium.render(f"Trial {trial_num}/20", True, BLACK)
        screen.blit(ready, (500 - ready.get_width()//2, 250))
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
        
        # Show letters
        show_letters(screen, seq_data['sequence'], trial_num)
        
        # Get recall
        recalled = get_recall(screen, trial_num)
        
        # Analyze
        analysis = analyze_trial(recalled, seq_data)
        results.append(analysis)
        
        # Brief feedback
        screen.fill(WHITE)
        score_text = font_medium.render(f"Score: {analysis['correct']}/7", True, BLACK)
        screen.blit(score_text, (500 - score_text.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    chunkable = [r for r in results if r['type'] == 'chunkable']
    random_trials = [r for r in results if r['type'] == 'random']
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (500 - title.get_width()//2, 150))
    
    chunk_acc = sum(t['accuracy'] for t in chunkable) / len(chunkable) * 100
    rand_acc = sum(t['accuracy'] for t in random_trials) / len(random_trials) * 100
    
    summary = [
        f"Chunkable: {chunk_acc:.1f}%",
        f"Random: {rand_acc:.1f}%",
        f"Difference: {chunk_acc - rand_acc:+.1f}%"
    ]
    
    y = 250
    for line in summary:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (500 - text.get_width()//2, y))
        y += 40
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save data
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()