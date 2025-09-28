import pygame
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Experiment 1: Primacy and Recency Effect")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Fixed list of 20 letters
LETTERS = ['K', 'Q', 'M', 'R', 'B', 'N', 'F', 'X', 'P', 'H', 
           'V', 'I', 'C', 'S', 'A', 'W', 'E', 'J', 'T', 'L']

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

def show_sequence(screen):
    """Show the 20-letter sequence"""
    print("Starting sequence...")
    
    for i, letter in enumerate(LETTERS):
        screen.fill(WHITE)
        
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_free_recall_input(screen, participant_name):
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
                elif event.unicode and event.unicode.isalpha() and len(current_input) == 0:
                    current_input = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Free Recall - {participant_name}", True, BLACK)
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

def analyze_primacy_recency(recalled_letters, original_sequence):
    """Analyze recall by serial position to identify primacy/recency effects"""
    
    # Create position mapping for each recalled letter
    position_recalls = []
    
    for recalled_letter in recalled_letters:
        # Find all positions where this letter appears in original sequence
        positions = [i for i, orig_letter in enumerate(original_sequence) if orig_letter == recalled_letter]
        
        # For each position found, record it (handling duplicates)
        for pos in positions:
            if pos not in [p['position'] for p in position_recalls]:
                position_recalls.append({
                    'letter': recalled_letter,
                    'position': pos,
                    'serial_position': pos + 1  # 1-indexed
                })
    
    # Calculate recall probability by position
    position_data = []
    for i in range(len(original_sequence)):
        was_recalled = any(pr['position'] == i for pr in position_recalls)
        position_data.append({
            'position': i + 1,
            'letter': original_sequence[i],
            'recalled': was_recalled
        })
    
    # Calculate primacy and recency scores
    primacy_positions = position_data[:5]  # First 5 positions
    middle_positions = position_data[5:15]  # Middle 10 positions
    recency_positions = position_data[15:]  # Last 5 positions
    
    primacy_score = sum(1 for p in primacy_positions if p['recalled']) / len(primacy_positions)
    middle_score = sum(1 for p in middle_positions if p['recalled']) / len(middle_positions)
    recency_score = sum(1 for p in recency_positions if p['recalled']) / len(recency_positions)
    
    results = {
        'position_data': position_data,
        'primacy_score': primacy_score,
        'middle_score': middle_score,
        'recency_score': recency_score,
        'total_recalled': len(position_recalls),
        'recall_by_position': [p['recalled'] for p in position_data]
    }
    
    return results

def show_results(screen, participant_name, analysis):
    """Show detailed results with primacy/recency analysis"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Primacy/Recency Results - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Main scores
        y_pos = 100
        scores = [
            f"Total letters recalled: {analysis['total_recalled']}/20",
            f"Primacy effect (positions 1-5): {analysis['primacy_score']*100:.1f}%",
            f"Middle positions (6-15): {analysis['middle_score']*100:.1f}%",
            f"Recency effect (positions 16-20): {analysis['recency_score']*100:.1f}%"
        ]
        
        for score in scores:
            text = font_small.render(score, True, BLACK)
            screen.blit(text, (50, y_pos))
            y_pos += 30
        
        # Serial position curve visualization (text-based)
        y_pos += 20
        curve_label = font_small.render("Serial Position Curve (✓ = recalled, ✗ = not recalled):", True, BLACK)
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
        
        # Effect interpretation
        y_pos += 80
        interpretation = font_small.render("Interpretation:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        if analysis['primacy_score'] > analysis['middle_score']:
            primacy_text = "✓ Primacy effect detected"
            primacy_color = GREEN
        else:
            primacy_text = "✗ No clear primacy effect"
            primacy_color = RED
        
        primacy_surface = font_small.render(primacy_text, True, primacy_color)
        screen.blit(primacy_surface, (50, y_pos))
        
        y_pos += 25
        if analysis['recency_score'] > analysis['middle_score']:
            recency_text = "✓ Recency effect detected"
            recency_color = GREEN
        else:
            recency_text = "✗ No clear recency effect"
            recency_color = RED
        
        recency_surface = font_small.render(recency_text, True, recency_color)
        screen.blit(recency_surface, (50, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"primacy_recency_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 1: Primacy and Recency Effect", True, BLACK)
        title_rect = title.get_rect(center=(400, 100))
        screen.blit(title, title_rect)
        
        instructions = [
            "You will see 20 letters, one at a time (1 second each)",
            "After the sequence, recall as many letters as possible",
            "Order doesn't matter - just recall what you remember",
            "We'll analyze recall by original position in the list",
            "This tests primacy (first items) and recency (last items) effects",
            "",
            "Press any key to start"
        ]
        
        y_pos = 180
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
        
        # Show countdown
        for count in [3, 2, 1]:
            screen.fill(WHITE)
            countdown = font_large.render(str(count), True, BLACK)
            countdown_rect = countdown.get_rect(center=(400, 300))
            screen.blit(countdown, countdown_rect)
            pygame.display.flip()
            time.sleep(1)
        
        # Show "GO!"
        screen.fill(WHITE)
        go_text = font_large.render("GO!", True, BLACK)
        go_rect = go_text.get_rect(center=(400, 300))
        screen.blit(go_text, go_rect)
        pygame.display.flip()
        time.sleep(1)
        
        # Show sequence
        show_sequence(screen)
        
        # Brief pause
        screen.fill(WHITE)
        pause_text = font_medium.render("Now recall all the letters you remember!", True, BLACK)
        pause_rect = pause_text.get_rect(center=(400, 300))
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()
        time.sleep(2)
        
        # Get free recall
        recalled_letters = get_free_recall_input(screen, participant_name)
        
        # Analyze for primacy/recency effects
        analysis = analyze_primacy_recency(recalled_letters, LETTERS)
        
        # Show results
        show_results(screen, participant_name, analysis)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'primacy_recency_effect',
            'original_sequence': LETTERS,
            'recalled_sequence': recalled_letters,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed primacy/recency test for {participant_name}")
        print(f"Primacy: {analysis['primacy_score']*100:.1f}%, Middle: {analysis['middle_score']*100:.1f}%, Recency: {analysis['recency_score']*100:.1f}%")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()