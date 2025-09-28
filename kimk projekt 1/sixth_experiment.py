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
font_xl = pygame.font.Font(None, 120)

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
        
        instruction = font_small.render("Press ENTER to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(500, 400))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
    
    return text.strip()

def generate_chunkable_sequences():
    """Generate 7-letter sequences with 4-letter words + 3 random letters vs random sequences"""
    
    # Common 4-letter words that people easily recognize
    four_letter_words = [
        'HAND', 'DOOR', 'BOOK', 'TREE', 'FACE', 'BLUE', 'COLD', 'DARK',
        'FAST', 'GOOD', 'HARD', 'HIGH', 'LAST', 'LONG', 'MAKE', 'NICE',
        'OPEN', 'PLAY', 'ROAD', 'SAFE', 'SOFT', 'TALK', 'WARM', 'WILD',
        'WORK', 'YEAR', 'GAME', 'HOME', 'JUMP', 'KEEP', 'LAND', 'LOVE',
        'MOVE', 'NAME', 'PART', 'SIDE', 'TAKE', 'TIME', 'TURN', 'WALK'
    ]
    
    # Random consonants for non-word portions
    random_consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    
    chunkable_sequences = []
    random_sequences = []
    
    # Generate 10 chunkable sequences (4-letter word + 3 random letters)
    for _ in range(10):
        # Choose a random 4-letter word
        word = random.choice(four_letter_words)
        
        # Generate 3 random consonants
        random_letters = [random.choice(random_consonants) for _ in range(3)]
        
        # Randomly place the word at start, middle, or end
        position = random.choice(['start', 'middle', 'end'])
        
        if position == 'start':
            # Word first: HAND + BXQ
            sequence = list(word) + random_letters
            word_positions = list(range(4))  # positions 0,1,2,3
        elif position == 'end':
            # Word last: BXQ + HAND
            sequence = random_letters + list(word)
            word_positions = list(range(3, 7))  # positions 3,4,5,6
        else:  # middle
            # Word in middle: B + HAND + XQ (if possible with 7 letters)
            # For 7 letters with 4-letter word, middle means 1 or 2 letters before
            if len(random_letters) >= 2:
                before = random_letters[:1]  # 1 letter before
                after = random_letters[1:]   # 2 letters after
                sequence = before + list(word) + after
                word_positions = list(range(1, 5))  # positions 1,2,3,4
            else:
                # Fallback to start position
                sequence = list(word) + random_letters
                word_positions = list(range(4))
        
        chunkable_sequences.append({
            'sequence': sequence,
            'word': word,
            'word_positions': word_positions,
            'word_position': position,
            'type': 'chunkable'
        })
    
    # Generate 10 random sequences (7 random consonants, no words)
    for _ in range(10):
        sequence = [random.choice(random_consonants) for _ in range(7)]
        random_sequences.append({
            'sequence': sequence,
            'word': None,
            'word_positions': [],
            'word_position': None,
            'type': 'random'
        })
    
    return chunkable_sequences, random_sequences

def show_letter_string(screen, letters, trial_num, condition, duration=3):
    """Show the 7-letter string all at once"""
    print(f"Showing {condition} sequence: {''.join(letters)} (trial {trial_num})")
    
    screen.fill(WHITE)
    
    # Show trial info
    trial_text = font_small.render(f"Trial {trial_num} - {condition.upper()} condition", True, BLUE)
    screen.blit(trial_text, (20, 20))
    
    # Display all 7 letters simultaneously with spacing
    letter_string = '  '.join(letters)  # Add spaces between letters for clarity
    string_surface = font_xl.render(letter_string, True, BLACK)
    string_rect = string_surface.get_rect(center=(500, 300))
    screen.blit(string_surface, string_rect)
    
    # Show duration countdown
    for remaining in range(duration, 0, -1):
        # Update timer display
        timer_rect = pygame.Rect(450, 400, 100, 50)
        pygame.draw.rect(screen, WHITE, timer_rect)
        
        timer_text = font_medium.render(str(remaining), True, RED)
        timer_text_rect = timer_text.get_rect(center=(500, 425))
        screen.blit(timer_text, timer_text_rect)
        
        pygame.display.flip()
        time.sleep(1)
        
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def get_string_recall_input(screen, participant_name, trial_num, condition):
    """Get recall of the 7-letter string"""
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
                            
                            if len(recalled_letters) >= 7:
                                input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if current_input:
                        current_input = current_input[:-1]
                    elif recalled_letters:
                        recalled_letters.pop()
                elif event.key == pygame.K_SPACE:
                    if current_input.strip():
                        letter = current_input.strip().upper()
                        if len(letter) == 1 and letter.isalpha():
                            recalled_letters.append(letter)
                            current_input = ""
                            
                            if len(recalled_letters) >= 7:
                                input_active = False
                elif event.key == pygame.K_ESCAPE:
                    # Allow early finish
                    input_active = False
                elif len(current_input) < 1 and event.unicode.isalpha():
                    current_input = event.unicode.upper()
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Recall Letters - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(500, 80))
        screen.blit(title, title_rect)
        
        trial_info = font_small.render(f"Trial {trial_num} ({condition}) - Enter 7 letters in order", True, BLACK)
        trial_rect = trial_info.get_rect(center=(500, 130))
        screen.blit(trial_info, trial_rect)
        
        instruction1 = font_small.render("Type each letter and press ENTER or SPACE", True, GRAY)
        instruction1_rect = instruction1.get_rect(center=(500, 160))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Backspace to remove letters | ESC to finish early", True, GRAY)
        instruction2_rect = instruction2.get_rect(center=(500, 185))
        screen.blit(instruction2, instruction2_rect)
        
        # Current input
        input_label = font_small.render(f"Position {len(recalled_letters) + 1}:", True, BLACK)
        screen.blit(input_label, (350, 250))
        
        input_surface = font_large.render(current_input + "|", True, BLACK)
        input_rect = input_surface.get_rect(center=(500, 300))
        screen.blit(input_surface, input_rect)
        
        # Show sequence entered so far
        sequence_label = font_small.render(f"Sequence entered ({len(recalled_letters)}/7):", True, BLACK)
        screen.blit(sequence_label, (50, 380))
        
        # Display letters in sequence boxes
        x_start = 50
        y_start = 420
        
        for i in range(7):
            x = x_start + i * 80
            
            # Draw position box
            box_color = GREEN if i < len(recalled_letters) else GRAY
            pygame.draw.rect(screen, box_color, (x, y_start, 70, 70), 3)
            
            # Draw position number
            pos_text = font_small.render(str(i + 1), True, BLACK)
            screen.blit(pos_text, (x + 30, y_start - 25))
            
            # Draw letter if entered
            if i < len(recalled_letters):
                letter_surface = font_medium.render(recalled_letters[i], True, BLACK)
                letter_rect = letter_surface.get_rect(center=(x + 35, y_start + 35))
                screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
    
    # Pad with empty strings if too short
    while len(recalled_letters) < 7:
        recalled_letters.append("")
    
    return recalled_letters[:7]

def analyze_chunking_effect(recalled_letters, original_data):
    """Analyze recall performance and chunking effects with word-based analysis"""
    
    original_letters = original_data['sequence']
    word = original_data['word']
    word_positions = original_data['word_positions']
    word_position = original_data['word_position']
    
    # Basic accuracy
    correct_positions = 0
    position_accuracy = []
    
    for i in range(7):
        if i < len(recalled_letters) and i < len(original_letters):
            correct = recalled_letters[i] == original_letters[i]
            position_accuracy.append(correct)
            if correct:
                correct_positions += 1
        else:
            position_accuracy.append(False)
    
    # Check if word was recalled as a unit (for chunkable sequences)
    word_intact = False
    word_accuracy = 0
    word_letters_correct = 0
    
    if word and word_positions:
        # Check each position in the word
        word_recalled_correctly = True
        for i, word_pos in enumerate(word_positions):
            if word_pos >= len(recalled_letters) or recalled_letters[word_pos] != word[i]:
                word_recalled_correctly = False
            else:
                word_letters_correct += 1
        
        word_intact = word_recalled_correctly
        word_accuracy = word_letters_correct / len(word) if word else 0
    
    # Analyze non-word letters (random letters) performance
    non_word_correct = 0
    non_word_total = 0
    
    for i in range(7):
        if word_positions and i not in word_positions:  # This is a random letter position
            non_word_total += 1
            if i < len(recalled_letters) and i < len(original_letters):
                if recalled_letters[i] == original_letters[i]:
                    non_word_correct += 1
    
    non_word_accuracy = non_word_correct / non_word_total if non_word_total > 0 else 0
    
    results = {
        'original_sequence': original_letters,
        'recalled_sequence': recalled_letters,
        'correct_positions': correct_positions,
        'total_positions': 7,
        'accuracy_rate': correct_positions / 7,
        'position_accuracy': position_accuracy,
        'word': word,
        'word_positions': word_positions,
        'word_position': word_position,
        'word_intact': word_intact,
        'word_accuracy': word_accuracy,
        'word_letters_correct': word_letters_correct,
        'non_word_accuracy': non_word_accuracy,
        'non_word_correct': non_word_correct,
        'non_word_total': non_word_total,
        'condition_type': original_data['type']
    }
    
    return results

def show_trial_results(screen, participant_name, analysis, trial_num):
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
        title_rect = title.get_rect(center=(500, 50))
        screen.blit(title, title_rect)
        
        # Condition and score
        condition_text = font_small.render(f"Condition: {analysis['condition_type'].upper()}", True, BLUE)
        screen.blit(condition_text, (50, 100))
        
        score_text = font_small.render(f"Score: {analysis['correct_positions']}/7 positions correct ({analysis['accuracy_rate']*100:.1f}%)", True, BLACK)
        screen.blit(score_text, (50, 130))
        
        # Chunk information
        if analysis['chunk']:
            chunk_text = font_small.render(f"Chunk: '{analysis['chunk']}' ({analysis['chunk_position']})", True, BLACK)
            screen.blit(chunk_text, (50, 160))
            
            if analysis['chunk_intact']:
                chunk_result = font_small.render("✓ Chunk recalled intact!", True, GREEN)
            else:
                chunk_result = font_small.render(f"✗ Chunk accuracy: {analysis['chunk_accuracy']*100:.1f}%", True, RED)
            screen.blit(chunk_result, (50, 190))
        
        # Show sequences
        y_pos = 240
        original_label = font_small.render("Original sequence:", True, BLACK)
        screen.blit(original_label, (50, y_pos))
        
        y_pos += 30
        for i, letter in enumerate(analysis['original_sequence']):
            x = 50 + i * 80
            
            # Highlight chunk letters if applicable
            if analysis['chunk'] and letter in analysis['chunk']:
                # Check if this position is part of the chunk
                chunk_letters = list(analysis['chunk'])
                chunk_length = len(chunk_letters)
                chunk_start_pos = 0
                if analysis['chunk_position'] == 'middle':
                    chunk_start_pos = (7 - chunk_length) // 2
                elif analysis['chunk_position'] == 'end':
                    chunk_start_pos = 7 - chunk_length
                
                if chunk_start_pos <= i < chunk_start_pos + chunk_length:
                    pygame.draw.rect(screen, BLUE, (x, y_pos, 70, 70), 5)
                else:
                    pygame.draw.rect(screen, GRAY, (x, y_pos, 70, 70), 3)
            else:
                pygame.draw.rect(screen, GRAY, (x, y_pos, 70, 70), 3)
            
            letter_surface = font_medium.render(letter, True, BLACK)
            letter_rect = letter_surface.get_rect(center=(x + 35, y_pos + 35))
            screen.blit(letter_surface, letter_rect)
        
        y_pos += 100
        recalled_label = font_small.render("Your recall:", True, BLACK)
        screen.blit(recalled_label, (50, y_pos))
        
        y_pos += 30
        for i, letter in enumerate(analysis['recalled_sequence']):
            x = 50 + i * 80
            
            # Color based on correctness
            if analysis['position_accuracy'][i]:
                color = GREEN
            else:
                color = RED
            
            pygame.draw.rect(screen, color, (x, y_pos, 70, 70), 3)
            
            if letter:  # Only show if not empty
                letter_surface = font_medium.render(letter, True, BLACK)
                letter_rect = letter_surface.get_rect(center=(x + 35, y_pos + 35))
                screen.blit(letter_surface, letter_rect)
        
        # Legend
        y_pos += 100
        legend_label = font_small.render("Legend:", True, BLACK)
        screen.blit(legend_label, (50, y_pos))
        
        y_pos += 25
        legend_items = [
            ("Blue outline = Chunk in original", BLUE),
            ("Green = Correct recall", GREEN), 
            ("Red = Incorrect recall", RED)
        ]
        
        for i, (text, color) in enumerate(legend_items):
            legend_text = font_small.render(text, True, color)
            screen.blit(legend_text, (50 + i * 200, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(500, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def analyze_chunking_experiment(all_trials):
    """Analyze overall chunking effect across all trials"""
    
    chunkable_trials = [t for t in all_trials if t['original_data']['type'] == 'chunkable']
    random_trials = [t for t in all_trials if t['original_data']['type'] == 'random']
    
    # Calculate average performance
    chunkable_accuracy = sum(t['analysis']['accuracy_rate'] for t in chunkable_trials) / len(chunkable_trials) if chunkable_trials else 0
    random_accuracy = sum(t['analysis']['accuracy_rate'] for t in random_trials) / len(random_trials) if random_trials else 0
    
    # Chunk intact rate
    chunks_intact = sum(1 for t in chunkable_trials if t['analysis']['chunk_intact'])
    chunk_intact_rate = chunks_intact / len(chunkable_trials) if chunkable_trials else 0
    
    # Chunking benefit
    chunking_benefit = chunkable_accuracy - random_accuracy
    
    results = {
        'chunkable_accuracy': chunkable_accuracy,
        'random_accuracy': random_accuracy,
        'chunking_benefit': chunking_benefit,
        'chunk_intact_rate': chunk_intact_rate,
        'chunks_intact': chunks_intact,
        'total_chunkable_trials': len(chunkable_trials),
        'total_random_trials': len(random_trials)
    }
    
    return results

def show_final_results(screen, participant_name, chunking_analysis, all_trials):
    """Show final chunking experiment results"""
    result_active = True
    
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        title = font_medium.render(f"Chunking Effect Results - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(500, 50))
        screen.blit(title, title_rect)
        
        # Main results
        y_pos = 120
        results_text = [
            f"Chunkable sequences: {chunking_analysis['chunkable_accuracy']*100:.1f}% accuracy",
            f"Random sequences: {chunking_analysis['random_accuracy']*100:.1f}% accuracy",
            f"Chunking benefit: {chunking_analysis['chunking_benefit']*100:+.1f}%",
            "",
            f"Chunks recalled intact: {chunking_analysis['chunks_intact']}/{chunking_analysis['total_chunkable_trials']} ({chunking_analysis['chunk_intact_rate']*100:.1f}%)"
        ]
        
        for text in results_text:
            if text == "":
                y_pos += 10
                continue
            color = BLACK
            if "benefit" in text:
                color = GREEN if chunking_analysis['chunking_benefit'] > 0 else RED
            
            text_surface = font_small.render(text, True, color)
            screen.blit(text_surface, (50, y_pos))
            y_pos += 25
        
        # Chunking effect interpretation
        y_pos += 30
        interpretation = font_small.render("Chunking Effect Analysis:", True, BLACK)
        screen.blit(interpretation, (50, y_pos))
        
        y_pos += 25
        if chunking_analysis['chunking_benefit'] > 0.1:
            effect_text = "✓ Strong chunking effect detected!"
            effect_color = GREEN
        elif chunking_analysis['chunking_benefit'] > 0.05:
            effect_text = "~ Moderate chunking effect"
            effect_color = BLUE
        else:
            effect_text = "✗ No clear chunking benefit"
            effect_color = RED
        
        effect_surface = font_small.render(effect_text, True, effect_color)
        screen.blit(effect_surface, (50, y_pos))
        
        y_pos += 25
        if chunking_analysis['chunk_intact_rate'] > 0.7:
            intact_text = "✓ Good at recognizing and using chunks"
            intact_color = GREEN
        elif chunking_analysis['chunk_intact_rate'] > 0.4:
            intact_text = "~ Some chunk recognition"
            intact_color = BLUE
        else:
            intact_text = "⚠ Difficulty using chunks effectively"
            intact_color = RED
        
        intact_surface = font_small.render(intact_text, True, intact_color)
        screen.blit(intact_surface, (50, y_pos))
        
        # Theory explanation
        y_pos += 50
        theory_label = font_small.render("Theory:", True, BLACK)
        screen.blit(theory_label, (50, y_pos))
        
        y_pos += 25
        theory_text = [
            "Chunking groups individual items into meaningful units",
            "This reduces working memory load (7 items → 2-3 chunks)",
            "Should see better recall for sequences with familiar chunks"
        ]
        
        for text in theory_text:
            theory_surface = font_small.render(text, True, GRAY)
            screen.blit(theory_surface, (50, y_pos))
            y_pos += 20
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(500, 570))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"experiment6_chunking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        title = font_medium.render("Experiment 6: Chunking Effect", True, BLACK)
        title_rect = title.get_rect(center=(500, 60))
        screen.blit(title, title_rect)
        
        instructions = [
            "This experiment tests the chunking effect on memory:",
            "",
            "• You'll see sequences of 7 letters presented ONE AT A TIME",
            "• Each letter shows for 1 second",
            "• After viewing, type the letters back in exact order",
            "• Some sequences contain real 4-letter WORDS (HAND, DOOR, etc.)",
            "• Others are completely random consonants",
            "",
            "Chunking theory predicts:",
            "• Better recall for sequences with real words",
            "• Words act as single chunks, reducing memory load",
            "• 7 random letters vs word+letters should show clear difference",
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
        
        # Generate sequences
        chunkable_sequences, random_sequences = generate_chunkable_sequences()
        
        # Combine and randomize all trials
        all_trials_data = chunkable_sequences + random_sequences
        random.shuffle(all_trials_data)
        
        # Run trials
        all_trials = []
        
        for i, trial_data in enumerate(all_trials_data):
            trial_num = i + 1
            
            # Show trial introduction
            screen.fill(WHITE)
            trial_intro = font_medium.render(f"Trial {trial_num}/20", True, BLACK)
            trial_rect = trial_intro.get_rect(center=(500, 250))
            screen.blit(trial_intro, trial_rect)
            
            ready_text = font_small.render("Press any key when ready", True, BLUE)
            ready_rect = ready_text.get_rect(center=(500, 320))
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
            
            # Show sequence letter by letter
            show_letter_sequence(screen, trial_data['sequence'], trial_num, trial_data['type'])
            
            # Brief pause before recall
            screen.fill(WHITE)
            pause_text = font_medium.render("Now enter the letters in order!", True, BLACK)
            pause_rect = pause_text.get_rect(center=(500, 300))
            screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            time.sleep(1)
            
            # Get recall
            recalled_letters = get_string_recall_input(screen, participant_name, trial_num, trial_data['type'])
            
            # Analyze trial
            analysis = analyze_chunking_effect(recalled_letters, trial_data)
            
            # Show trial results
            show_trial_results(screen, participant_name, analysis, trial_num)
            
            # Store trial data
            trial_result = {
                'trial_number': trial_num,
                'original_data': trial_data,
                'recalled_letters': recalled_letters,
                'analysis': analysis
            }
            all_trials.append(trial_result)
        
        # Analyze overall chunking effect
        chunking_analysis = analyze_chunking_experiment(all_trials)
        
        # Show final results
        show_final_results(screen, participant_name, chunking_analysis, all_trials)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment': 'chunking_effect',
            'all_trials': all_trials,
            'chunking_analysis': chunking_analysis,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed chunking experiment for {participant_name}")
        print(f"Chunking benefit: {chunking_analysis['chunking_benefit']*100:+.1f}%")
        print(f"Chunks intact: {chunking_analysis['chunks_intact']}/{chunking_analysis['total_chunkable_trials']}")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()