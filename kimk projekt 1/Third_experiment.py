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

def generate_consonant_sequence(length=15):
    """Generate a random sequence of unique consonants (no vowels, no repeats)"""
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

def show_sequence(screen, letters, condition, trial_num):
    """Show the letter sequence"""
    for i, letter in enumerate(letters):
        screen.fill(WHITE)
        
        info_text = font_small.render(f"Trial {trial_num}/20 - {condition.upper()} - Letter {i+1}/15", True, BLUE)
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

def counting_task(screen, duration=20):
    """Counting backwards distraction task"""
    start_time = time.time()
    
    # Show instructions
    screen.fill(WHITE)
    title = font_medium.render("Distraction Task", True, BLACK)
    screen.blit(title, (400 - title.get_width()//2, 120))
    
    instruction1 = font_small.render("Count backwards from 100 by 3s", True, BLACK)
    screen.blit(instruction1, (400 - instruction1.get_width()//2, 180))
    
    instruction2 = font_small.render("Example: 100, 97, 94, 91...", True, GRAY)
    screen.blit(instruction2, (400 - instruction2.get_width()//2, 210))
    
    instruction3 = font_small.render("Type each number and press ENTER", True, BLACK)
    screen.blit(instruction3, (400 - instruction3.get_width()//2, 260))
    
    ready = font_small.render("Press any key to start", True, BLUE)
    screen.blit(ready, (400 - ready.get_width()//2, 320))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    # Counting task
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
                        numbers_entered.append(int(current_input.strip()))
                        current_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.unicode.isdigit():
                    current_input += event.unicode
        
        screen.fill(WHITE)
        
        elapsed = time.time() - start_time
        remaining = max(0, duration - elapsed)
        timer = font_medium.render(f"Time: {remaining:.0f}s", True, RED)
        screen.blit(timer, (400 - timer.get_width()//2, 80))
        
        instruction = font_small.render("Count backwards from 100 by 3s", True, BLACK)
        screen.blit(instruction, (400 - instruction.get_width()//2, 140))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        screen.blit(input_surface, (400 - input_surface.get_width()//2, 240))
        
        if numbers_entered:
            last_nums = ", ".join(map(str, numbers_entered[-5:]))
            nums_text = font_small.render(f"Last: {last_nums}", True, GRAY)
            screen.blit(nums_text, (50, 380))
        
        # Progress bar
        bar_width = 600
        bar_x = 100
        bar_y = 500
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, 15))
        progress = (duration - remaining) / duration
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), 15))
        
        pygame.display.flip()
        
        if remaining <= 0:
            break
    
    # Calculate correct sequence
    correct_count = 0
    expected = 100
    for num in numbers_entered:
        if num == expected:
            correct_count += 1
            expected -= 3
        else:
            break
    
    return {
        'count': len(numbers_entered),
        'correct': correct_count
    }

def get_free_recall(screen, condition, trial_num):
    """Get free recall input"""
    recalled = []
    current = ""
    time_limit = 90
    start_time = time.time()
    
    while True:
        remaining = max(0, time_limit - (time.time() - start_time))
        
        if remaining <= 0:
            break
        
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
                    current = current[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return recalled
                elif len(current) < 1 and event.unicode.isalpha():
                    current = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Trial {trial_num} Recall - {condition.upper()}", True, BLACK)
        screen.blit(title, (400 - title.get_width()//2, 60))
        
        instruction = font_small.render("Type letters (any order) | ENTER/SPACE | ESC when done", True, GRAY)
        screen.blit(instruction, (400 - instruction.get_width()//2, 120))
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer = font_medium.render(f"{minutes:02d}:{seconds:02d}", True, RED)
        screen.blit(timer, (400 - timer.get_width()//2, 170))
        
        input_surface = font_large.render(current + "|", True, BLACK)
        screen.blit(input_surface, (400 - input_surface.get_width()//2, 240))
        
        recall_label = font_small.render(f"Recalled ({len(recalled)}):", True, BLACK)
        screen.blit(recall_label, (50, 340))
        
        x, y = 50, 370
        for i, letter in enumerate(recalled):
            if i > 0 and i % 15 == 0:
                y += 30
                x = 50
            letter_surf = font_medium.render(letter, True, BLACK)
            screen.blit(letter_surf, (x, y))
            x += 35
        
        bar_width = 700
        bar_x = 50
        bar_y = 550
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, 15))
        progress = remaining / time_limit
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, int(bar_width * progress), 15))
        
        pygame.display.flip()
    
    return recalled

def analyze_recall(recalled, original):
    """Analyze recall performance"""
    unique_correct = len(set(recalled) & set(original))
    
    # Position analysis
    position_data = []
    for i, letter in enumerate(original):
        recalled_it = letter in recalled
        position_data.append({
            'position': i + 1,
            'letter': letter,
            'recalled': recalled_it
        })
    
    # Primacy, middle, recency (adjusted for 15 items)
    primacy = position_data[:5]
    middle = position_data[5:10]
    recency = position_data[10:]
    
    return {
        'total_recalled': len(recalled),
        'unique_correct': unique_correct,
        'recall_rate': unique_correct / len(original),
        'primacy': sum(1 for p in primacy if p['recalled']) / len(primacy),
        'middle': sum(1 for p in middle if p['recalled']) / len(middle),
        'recency': sum(1 for p in recency if p['recalled']) / len(recency)
    }

def save_data(participant_name, trials):
    """Save data to JSON"""
    filename = f"exp3_{participant_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    control = [t for t in trials if t['condition'] == 'control']
    distraction = [t for t in trials if t['condition'] == 'distraction']
    
    data = {
        'participant': participant_name,
        'timestamp': datetime.now().isoformat(),
        'trials': trials,
        'summary': {
            'control_recall': sum(t['recall_rate'] for t in control) / len(control),
            'distraction_recall': sum(t['recall_rate'] for t in distraction) / len(distraction),
            'working_memory_effect': (sum(t['recall_rate'] for t in control) / len(control)) - 
                                    (sum(t['recall_rate'] for t in distraction) / len(distraction)),
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
        "Experiment 3: Working Memory Task",
        "",
        "20 trials (10 control, 10 distraction)",
        "",
        "CONTROL: See 15 letters → recall immediately",
        "DISTRACTION: See 15 letters → counting task → recall",
        "",
        "Counting task: Count backwards from 100 by 3s",
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
    
    # Create trial list
    trial_list = ['control'] * 10 + ['distraction'] * 10
    random.shuffle(trial_list)
    
    results = []
    
    # Run 20 trials
    for i, condition in enumerate(trial_list):
        trial_num = i + 1
        
        # Ready screen
        screen.fill(WHITE)
        ready_title = font_medium.render(f"Trial {trial_num}/20: {condition.upper()}", True, BLACK)
        screen.blit(ready_title, (400 - ready_title.get_width()//2, 220))
        
        instruction = font_small.render("Press any key when ready", True, BLUE)
        screen.blit(instruction, (400 - instruction.get_width()//2, 280))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        
        # Generate and show sequence
        letters = generate_consonant_sequence(15)
        show_sequence(screen, letters, condition, trial_num)
        
        # Distraction or immediate recall
        counting_perf = None
        if condition == 'distraction':
            counting_perf = counting_task(screen, 20)
        
        # Recall
        recalled = get_free_recall(screen, condition, trial_num)
        
        # Analyze
        analysis = analyze_recall(recalled, letters)
        
        # Store
        results.append({
            'trial': trial_num,
            'condition': condition,
            'original': letters,
            'recalled': recalled,
            'recall_rate': analysis['recall_rate'],
            'primacy': analysis['primacy'],
            'middle': analysis['middle'],
            'recency': analysis['recency'],
            'counting': counting_perf
        })
        
        # Feedback
        screen.fill(WHITE)
        score = font_medium.render(f"Recalled: {analysis['unique_correct']}/15", True, BLACK)
        screen.blit(score, (400 - score.get_width()//2, 280))
        pygame.display.flip()
        time.sleep(1.5)
    
    # Final summary
    control = [r for r in results if r['condition'] == 'control']
    distraction = [r for r in results if r['condition'] == 'distraction']
    
    control_rate = sum(t['recall_rate'] for t in control) / len(control) * 100
    distraction_rate = sum(t['recall_rate'] for t in distraction) / len(distraction) * 100
    effect = control_rate - distraction_rate
    
    screen.fill(WHITE)
    title = font_medium.render("Experiment Complete!", True, BLACK)
    screen.blit(title, (400 - title.get_width()//2, 150))
    
    summary = [
        f"Control: {control_rate:.1f}%",
        f"Distraction: {distraction_rate:.1f}%",
        f"Effect: {effect:+.1f}%"
    ]
    
    y = 250
    for line in summary:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (400 - text.get_width()//2, y))
        y += 40
    
    if effect > 10:
        interpretation = "Strong working memory effect!"
        color = RED
    elif effect > 5:
        interpretation = "Moderate effect"
        color = BLUE
    else:
        interpretation = "Minimal effect"
        color = GRAY
    
    interp = font_small.render(interpretation, True, color)
    screen.blit(interp, (400 - interp.get_width()//2, y + 30))
    
    pygame.display.flip()
    time.sleep(3)
    
    # Save
    save_data(participant_name, results)
    
    pygame.quit()

if __name__ == "__main__":
    main()