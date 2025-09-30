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

# Word list for chunking
FOUR_LETTER_WORDS = [
    'HAND', 'DOOR', 'BOOK', 'TREE', 'FACE', 'BLUE', 'COLD', 'DARK',
    'FAST', 'GOOD', 'HARD', 'HIGH', 'LAST', 'LONG', 'MAKE', 'NICE',
    'OPEN', 'PLAY', 'ROAD', 'SAFE', 'SOFT', 'TALK', 'WARM', 'WILD',
    'WORK', 'YEAR', 'GAME', 'HOME', 'JUMP', 'KEEP', 'LAND', 'LOVE',
    'MOVE', 'NAME', 'PART', 'SIDE', 'TAKE', 'TIME', 'TURN', 'WALK',
    'BIRD', 'CAKE', 'DESK', 'FARM', 'GATE', 'HILL', 'KING', 'LAMP',
    'MAIL', 'PARK', 'RAIN', 'SAND', 'TENT', 'WAVE', 'WIND', 'GIFT'
]

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

def generate_chunkable_sequence():
    """Generate sequence with a 4-letter word + 3 random unique consonants"""
    word = random.choice(FOUR_LETTER_WORDS)
    word_letters = list(word)
    
    # Get consonants not in the word
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    available = [c for c in consonants if c not in word_letters]
    random_letters = random.sample(available, 3)
    
    # Randomly place word at start or end
    if random.choice([True, False]):
        sequence = word_letters + random_letters  # Word first
        word_position = 'start'
    else:
        sequence = random_letters + word_letters  # Word last
        word_position = 'end'
    
    return {
        'sequence': sequence,
        'word': word,
        'word_position': word_position,
        'type': 'chunkable'
    }

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
        
        instruction = font_small.render("Type letters in order and press ENTER/SPACE", True, GRAY)
        screen.blit(instruction, (500 - instruction.get_width()//2, 130))
        
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

def analyze_chunking(recalled, original_data):
    """Analyze if the word chunk was recalled"""
    original = original_data['sequence']
    word = original_data['word']
    
    # Check position accuracy
    correct = sum(1 for i in range(7) if i < len(recalled) and recalled[i] == original[i])
    
    # Check if word was recalled as a unit
    word_intact = False
    if original_data['word_position'] == 'start':
        # Word at positions 0-3
        word_intact = all(i < len(recalled) and recalled[i] == word[i] for i in range(4))
    else:  # end
        # Word at positions 3-6
        word_intact = all(i < len(recalled) and recalled[i+3] == word[i] for i in range(4))
    
    return {
        'original': original,
        'recalled': recalled,
        'correct': correct,
        'accuracy': correct / 7,
        'word': word,
        'word_intact': word_intact,
        'word_position': original_data['word_position']
    }

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp6_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
        'trials': trials,
        'summary': {
            'average_accuracy': sum(t['accuracy'] for t in trials) / len(trials),
            'words_intact_rate': sum(1 for t in trials if t['word_intact']) / len(trials),
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
        "Experiment 6: Chunking Effect",
        "",
        "20 trials - ALL with 4-letter words",
        "",
        "Each sequence contains a real English word!",
        "Examples: HAND, DOOR, TREE, BOOK...",
        "",
        "7 letters per trial (1 sec each)",
        "Recall them in order",
        "",
        "Press any key to start"
    ]
    
    y = 110
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
    
    # Run 20 trials (all chunkable)
    for trial_num in range(1, 21):
        # Generate NEW chunkable sequence each trial
        seq_data = generate_chunkable_sequence()
        
        # Ready screen
        screen.fill(WHITE)
        ready_title = font_medium.render(f"Trial {trial_num}/20", True, BLACK)
        screen.blit(ready_title, (500 - ready_title.get_width()//2, 240))
        
        hint = font_small.render("(This sequence contains a 4-letter word)", True, GRAY)
        screen.blit(hint, (500 - hint.get_width()//2, 280))
        
        instruction = font_small.render("Press any key when ready", True, BLUE)
        screen.blit(instruction, (500 - instruction.get_width()//2, 330))
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
        analysis = analyze_chunking(recalled, seq_data)
        
        # Store
        results.append({
            'trial': trial_num,
            'original': analysis['original'],
            'recalled': analysis['recalled'],
            'correct': analysis['correct'],
            'accuracy': analysis['accuracy'],
            'word': analysis['word'],
            'word_intact': analysis['word_intact'],
            'word_position': analysis['word_position']
        })
        
        # Brief feedback showing the word
        screen.fill(WHITE)
        score = font_medium.render(f"Score: {analysis['correct']}/7", True, BLACK)
        screen.blit(score, (500 - score.get_width()//2, 240))
        
        word_text = font_small.render(f"The word was: {analysis['word']}", True, BLUE)
        screen.blit(word_text, (500 - word_text.get_width()//2, 300))
        
        if analysis['word_intact']:
            intact_text = font_small.render("✓ You recalled the word perfectly!", True, GREEN)
        else:
            intact_text = font_small.render("The word wasn't fully recalled", True, RED)
        screen.blit(intact_text, (500 - intact_text.get_width()//2, 340))
        
        pygame.display.flip()
        time.sleep(2.5)
    
    # Final summary
    avg_acc = sum(t['accuracy'] for t in results) / len(results) * 100
    words_intact = sum(1 for t in results if t['word_intact'])
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (500 - title.get_width()//2, 150))
    
    summary = [
        f"Average accuracy: {avg_acc:.1f}%",
        f"Words recalled intact: {words_intact}/20"
    ]
    
    y = 240
    for line in summary:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (500 - text.get_width()//2, y))
        y += 35
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()