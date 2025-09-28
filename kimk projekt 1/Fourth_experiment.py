import pygame
import time
import json
from datetime import datetime
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Delayed Memory Experiment")
font_large = pygame.font.Font(None, 200)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Generate random consonant sequences for each trial
def generate_consonant_sequence(length=20):
    """Generate a random sequence of consonants (no vowels to avoid chunks)"""
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'  # Exclude vowels A, E, I, O, U
    return [random.choice(consonants) for _ in range(length)]

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
        
        # Draw screen
        screen.fill(WHITE)
        
        # Draw prompt
        prompt_surface = font_medium.render(prompt, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(400, 250))
        screen.blit(prompt_surface, prompt_rect)
        
        # Draw text input
        text_surface = font_medium.render(text + "|", True, BLACK)
        text_rect = text_surface.get_rect(center=(400, 320))
        screen.blit(text_surface, text_rect)
        
        # Instructions
        instruction = font_small.render("Press ENTER to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 400))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
    
    return text.strip()

def show_sequence(screen, letters):
    """Show the 20-letter sequence"""
    print("Starting sequence...")
    
    for i, letter in enumerate(letters):
        # Clear screen
        screen.fill(WHITE)
        
        # Draw letter
        letter_surface = font_large.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(400, 300))
        screen.blit(letter_surface, letter_rect)
        
        pygame.display.flip()
        
        # Wait 1 second
        time.sleep(1)
        
        # Check for quit events during sequence
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def show_delay_period(screen, participant_name):
    """Show 60-second delay with countdown"""
    print("Starting 60-second delay period...")
    
    delay_time = 60  # 60 seconds
    
    for remaining in range(delay_time, 0, -1):
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Clear screen
        screen.fill(WHITE)
        
        # Title
        title = font_medium.render(f"Delay Period - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 150))
        screen.blit(title, title_rect)
        
        # Instructions
        instruction1 = font_small.render("Please wait before the memory test begins", True, BLACK)
        instruction1_rect = instruction1.get_rect(center=(400, 220))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_small.render("Try to remember the sequence of letters you saw", True, BLUE)
        instruction2_rect = instruction2.get_rect(center=(400, 260))
        screen.blit(instruction2, instruction2_rect)
        
        # Countdown timer
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        timer_surface = font_large.render(timer_text, True, RED)
        timer_rect = timer_surface.get_rect(center=(400, 350))
        screen.blit(timer_surface, timer_rect)
        
        # Progress bar
        progress_width = 400
        progress_height = 20
        progress_x = 200
        progress_y = 450
        
        # Background bar
        pygame.draw.rect(screen, (200, 200, 200), (progress_x, progress_y, progress_width, progress_height))
        
        # Progress fill
        progress_fill = (delay_time - remaining) / delay_time
        fill_width = int(progress_width * progress_fill)
        pygame.draw.rect(screen, RED, (progress_x, progress_y, fill_width, progress_height))
        
        # Time remaining text
        remaining_text = font_small.render(f"Time remaining: {remaining} seconds", True, BLACK)
        remaining_rect = remaining_text.get_rect(center=(400, 500))
        screen.blit(remaining_text, remaining_rect)
        
        pygame.display.flip()
        time.sleep(1)
    
    # Show "Time's up!" message
    screen.fill(WHITE)
    
    times_up = font_medium.render("Time's up! Get ready for the memory test...", True, RED)
    times_up_rect = times_up.get_rect(center=(400, 300))
    screen.blit(times_up, times_up_rect)
    
    pygame.display.flip()
    time.sleep(2)

def run_test(screen, participant_name, letters):
    """Run the memory test"""
    print(f"Starting test for {participant_name}")
    answers = []
    
    for i in range(20):
        # Get answer for position i+1
        prompt = f"Position {i+1} - What letter? (Participant: {participant_name})"
        answer = get_text_input(screen, prompt)
        
        correct_letter = letters[i]
        is_correct = answer.upper() == correct_letter
        
        answers.append({
            'position': i + 1,
            'correct': correct_letter,
            'answer': answer.upper(),
            'is_correct': is_correct
        })
    
    return answers

def show_results(screen, participant_name, answers, trial_num):
    """Show results for individual trial"""
    correct_count = sum(1 for a in answers if a['is_correct'])
    accuracy = (correct_count / 20) * 100
    
    result_active = True
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        # Title
        title = font_medium.render(f"Trial {trial_num} Results - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 100))
        screen.blit(title, title_rect)
        
        # Delay info
        delay_info = font_small.render("(60-second delay between sequence and test)", True, BLUE)
        delay_rect = delay_info.get_rect(center=(400, 140))
        screen.blit(delay_info, delay_rect)
        
        # Score
        score = font_medium.render(f"Score: {correct_count}/20 ({accuracy:.1f}%)", True, BLACK)
        score_rect = score.get_rect(center=(400, 200))
        screen.blit(score, score_rect)
        
        # Show some details (first 10 answers)
        y_pos = 280
        for i in range(min(10, len(answers))):
            answer = answers[i]
            color = GREEN if answer['is_correct'] else RED
            text = f"Pos {answer['position']}: {answer['correct']} -> {answer['answer']}"
            detail = font_small.render(text, True, color)
            screen.blit(detail, (200, y_pos))
            y_pos += 25
        
        # Show remaining answers if there are more than 10
        if len(answers) > 10:
            more_text = font_small.render("... and 10 more answers", True, BLACK)
            screen.blit(more_text, (200, y_pos))
        
        # Instructions
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 550))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def show_final_summary(screen, participant_name, all_trials, overall_accuracy):
    """Show final summary of all trials"""
    result_active = True
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                result_active = False
        
        screen.fill(WHITE)
        
        # Title
        title = font_medium.render(f"Final Summary - {participant_name}", True, BLACK)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        # Overall performance
        summary = font_medium.render(f"Overall: {len(all_trials)} trials, {overall_accuracy:.1f}% accuracy", True, BLACK)
        summary_rect = summary.get_rect(center=(400, 140))
        screen.blit(summary, summary_rect)
        
        # Trial-by-trial breakdown
        y_pos = 200
        breakdown_label = font_small.render("Trial breakdown:", True, BLACK)
        screen.blit(breakdown_label, (50, y_pos))
        
        y_pos += 30
        for i, trial in enumerate(all_trials):
            if i < 10:  # Show first 10 trials
                trial_text = f"Trial {trial['trial_number']}: {trial['score']}/20 ({trial['accuracy']:.1f}%)"
                trial_surface = font_small.render(trial_text, True, BLACK)
                screen.blit(trial_surface, (50, y_pos))
                y_pos += 20
        
        if len(all_trials) > 10:
            more_text = font_small.render(f"... and {len(all_trials) - 10} more trials", True, GRAY)
            screen.blit(more_text, (50, y_pos))
        
        # Best and worst performance
        best_trial = max(all_trials, key=lambda t: t['accuracy'])
        worst_trial = min(all_trials, key=lambda t: t['accuracy'])
        
        y_pos += 50
        best_text = font_small.render(f"Best trial: {best_trial['accuracy']:.1f}% (Trial {best_trial['trial_number']})", True, GREEN)
        screen.blit(best_text, (50, y_pos))
        
        y_pos += 25
        worst_text = font_small.render(f"Worst trial: {worst_trial['accuracy']:.1f}% (Trial {worst_trial['trial_number']})", True, RED)
        screen.blit(worst_text, (50, y_pos))
        
        instruction = font_small.render("Press any key to continue", True, BLUE)
        instruction_rect = instruction.get_rect(center=(400, 550))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()

def save_data(all_results):
    """Save all results to JSON file"""
    filename = f"delayed_memory_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"Data saved to {filename}")

def main():
    """Main game loop"""
    all_results = []
    
    while True:
        # Run multiple trials
        trials_per_participant = 20  # 20 trials with 60-second delay each
        all_trials = []
        
        for trial_num in range(1, trials_per_participant + 1):
            # Generate new random sequence for each trial
            letters = generate_consonant_sequence(20)
            
            # Show trial introduction
            screen.fill(WHITE)
            trial_intro = font_medium.render(f"Trial {trial_num}/{trials_per_participant}", True, BLACK)
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
            show_sequence(screen, letters)
            
            # 60-second delay period
            show_delay_period(screen, participant_name)
            
            # Run test
            answers = run_test(screen, participant_name, letters)
            
            # Show results for this trial
            show_results(screen, participant_name, answers, trial_num)
            
            # Save trial data
            trial_data = {
                'trial_number': trial_num,
                'letters': letters,
                'answers': answers,
                'score': sum(1 for a in answers if a['is_correct']),
                'accuracy': (sum(1 for a in answers if a['is_correct']) / 20) * 100
            }
            all_trials.append(trial_data)
            
            print(f"Completed trial {trial_num} for {participant_name}")
        
        # Calculate overall performance
        total_correct = sum(trial['score'] for trial in all_trials)
        total_possible = len(all_trials) * 20
        overall_accuracy = (total_correct / total_possible) * 100
        
        # Show final summary
        show_final_summary(screen, participant_name, all_trials, overall_accuracy)
        
        # Save participant data
        participant_data = {
            'name': participant_name,
            'experiment_type': 'delayed_memory_60s_multiple_trials',
            'delay_seconds': 60,
            'all_trials': all_trials,
            'trials_completed': len(all_trials),
            'total_correct': total_correct,
            'total_possible': total_possible,
            'overall_accuracy': overall_accuracy,
            'timestamp': datetime.now().isoformat()
        }
        all_results.append(participant_data)
        
        print(f"Completed delayed test for {participant_name}")
    
    # Save all data before quitting
    if all_results:
        save_data(all_results)
    
    pygame.quit()

if __name__ == "__main__":
    main()