"""
Visualization module for Disk Scheduling Algorithms
Creates graphs showing performance comparison and head movement
"""

import matplotlib.pyplot as plt
import numpy as np
from disk_scheduling import DiskScheduler
import matplotlib.patches as mpatches


def plot_comparison_bar(scheduler, results):
    """Create bar chart comparing total movement of algorithms"""
    algorithms = list(results.keys())
    movements = [results[alg][0] for alg in algorithms]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, movements, color=colors, edgecolor='black', linewidth=2, width=0.6)
    
    # Add value labels on bars
    for bar, movement in zip(bars, movements):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(movement)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Disk Scheduling Algorithm', fontsize=12, fontweight='bold')
    plt.ylabel('Total Head Movement (cylinders)', fontsize=12, fontweight='bold')
    plt.title('Disk Scheduling Algorithms - Performance Comparison\n' +
             f'({scheduler.num_requests} requests, {scheduler.num_cylinders} cylinders)',
             fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    return plt.gcf()


def plot_head_position_movements(scheduler, results, max_points=500):
    """Create line plots showing head position over time for each algorithm"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    algorithms = list(results.keys())
    
    for idx, (ax, algorithm, color) in enumerate(zip(axes, algorithms, colors)):
        positions = results[algorithm][1]
        total_movement = results[algorithm][0]
        
        # Sample points if too many (for cleaner visualization)
        if len(positions) > max_points:
            sample_indices = np.linspace(0, len(positions) - 1, max_points, dtype=int)
            sampled_positions = [positions[i] for i in sample_indices]
            x_data = sample_indices
        else:
            sampled_positions = positions
            x_data = range(len(positions))
        
        ax.plot(x_data, sampled_positions, color=color, linewidth=1.5, alpha=0.8)
        ax.scatter(x_data[0], sampled_positions[0], color='green', s=100, zorder=5, label='Start', marker='o')
        ax.scatter(x_data[-1], sampled_positions[-1], color='red', s=100, zorder=5, label='End', marker='x')
        
        ax.set_xlabel('Request Number', fontsize=11, fontweight='bold')
        ax.set_ylabel('Head Position (cylinder)', fontsize=11, fontweight='bold')
        ax.set_title(f'{algorithm}\nTotal Movement: {total_movement} cylinders',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best')
        ax.set_ylim(-100, scheduler.num_cylinders + 100)
    
    plt.tight_layout()
    return fig


def plot_performance_metrics(scheduler, results):
    """Create a more detailed performance comparison visualization"""
    algorithms = list(results.keys())
    movements = [results[alg][0] for alg in algorithms]
    
    # Calculate additional metrics
    avg_movements = []
    for algorithm in algorithms:
        positions = results[algorithm][1]
        movements_list = [abs(positions[i] - positions[i-1]) for i in range(1, len(positions))]
        avg_movements.append(np.mean(movements_list) if movements_list else 0)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Total movement
    bars1 = ax1.bar(algorithms, movements, color=colors, edgecolor='black', linewidth=2, width=0.6)
    for bar, movement in zip(bars1, movements):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(movement)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Total Head Movement (cylinders)', fontsize=11, fontweight='bold')
    ax1.set_title('Total Head Movement by Algorithm', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Average movement per request
    bars2 = ax2.bar(algorithms, avg_movements, color=colors, edgecolor='black', linewidth=2, width=0.6)
    for bar, avg_movement in zip(bars2, avg_movements):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{avg_movement:.2f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Average Movement per Request (cylinders)', fontsize=11, fontweight='bold')
    ax2.set_title('Average Head Movement per Request', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig


def plot_efficiency_comparison(scheduler, results):
    """Create a visualization comparing efficiency of algorithms"""
    algorithms = list(results.keys())
    movements = [results[alg][0] for alg in algorithms]
    
    # Normalize to percentage (best algorithm = 100%)
    best_movement = min(movements)
    efficiency = [100 * (best_movement / m) for m in movements]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = ax.barh(algorithms, efficiency, color=colors, edgecolor='black', linewidth=2, height=0.6)
    
    # Add percentage labels
    for bar, eff in zip(bars, efficiency):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f'{eff:.1f}%',
               ha='left', va='center', fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('Efficiency (relative to best algorithm)', fontsize=12, fontweight='bold')
    ax.set_title(f'Algorithm Efficiency Comparison\n(100% = Best performing algorithm)',
                fontsize=13, fontweight='bold')
    ax.set_xlim(0, 110)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig


def create_summary_report(scheduler, results):
    """Create a comprehensive summary report visualization"""
    algorithms = list(results.keys())
    movements = [results[alg][0] for alg in algorithms]
    
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # 1. Main comparison (large, top-left and right)
    ax1 = fig.add_subplot(gs[0, :])
    bars = ax1.bar(algorithms, movements, color=colors, edgecolor='black', linewidth=2.5, width=0.5)
    for bar, movement in zip(bars, movements):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(movement)} cyl',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Total Head Movement (cylinders)', fontsize=11, fontweight='bold')
    ax1.set_title('Disk Scheduling Algorithms - Total Head Movement Comparison',
                 fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 2. Efficiency (bottom-left)
    ax2 = fig.add_subplot(gs[1, 0])
    best_movement = min(movements)
    efficiency = [100 * (best_movement / m) for m in movements]
    bars2 = ax2.barh(algorithms, efficiency, color=colors, edgecolor='black', linewidth=2)
    for bar, eff in zip(bars2, efficiency):
        width = bar.get_width()
        ax2.text(width - 5, bar.get_y() + bar.get_height()/2.,
                f'{eff:.1f}%',
                ha='right', va='center', fontsize=10, fontweight='bold', color='white')
    ax2.set_xlabel('Efficiency (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Relative Efficiency', fontsize=11, fontweight='bold')
    ax2.set_xlim(0, 110)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 3. Statistics table (bottom-right)
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axis('off')
    
    # Create statistics text
    best_idx = movements.index(best_movement)
    worst_idx = movements.index(max(movements))
    
    stats_text = f"""
    SIMULATION PARAMETERS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Total Cylinders: {scheduler.num_cylinders}
    Number of Requests: {scheduler.num_requests}
    Initial Head Position: {scheduler.initial_position}
    
    RESULTS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Best Algorithm: {algorithms[best_idx]}
    Total Movement: {int(movements[best_idx])} cylinders
    
    Worst Algorithm: {algorithms[worst_idx]}
    Total Movement: {int(movements[worst_idx])} cylinders
    
    Difference: {int(movements[worst_idx] - movements[best_idx])} cylinders
    Improvement: {((movements[worst_idx] - movements[best_idx]) / movements[worst_idx] * 100):.1f}%
    """
    
    ax3.text(0.1, 0.5, stats_text, transform=ax3.transAxes,
            fontsize=10, verticalalignment='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle(f'Disk Scheduling Algorithms - Comprehensive Report',
                fontsize=14, fontweight='bold', y=0.98)
    
    return fig


def save_all_plots(scheduler, results, output_dir='results'):
    """Save all plots to files"""
    import os
    
    # Create results directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\nSaving visualizations to '{output_dir}/' directory...")
    
    # Plot 1: Bar chart comparison
    fig1 = plot_comparison_bar(scheduler, results)
    fig1.savefig(f'{output_dir}/1_comparison_bar.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/1_comparison_bar.png")
    
    # Plot 2: Head position movements
    fig2 = plot_head_position_movements(scheduler, results)
    fig2.savefig(f'{output_dir}/2_head_movements.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/2_head_movements.png")
    
    # Plot 3: Performance metrics
    fig3 = plot_performance_metrics(scheduler, results)
    fig3.savefig(f'{output_dir}/3_performance_metrics.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/3_performance_metrics.png")
    
    # Plot 4: Efficiency comparison
    fig4 = plot_efficiency_comparison(scheduler, results)
    fig4.savefig(f'{output_dir}/4_efficiency_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/4_efficiency_comparison.png")
    
    # Plot 5: Summary report
    fig5 = create_summary_report(scheduler, results)
    fig5.savefig(f'{output_dir}/5_summary_report.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/5_summary_report.png")
    
    plt.close('all')
    print(f"\n✓ All visualizations saved successfully!\n")


def main():
    """Main function for visualization"""
    from disk_scheduling import DiskScheduler, print_results
    
    # Parameters
    NUM_CYLINDERS = 5000
    NUM_REQUESTS = 1000
    INITIAL_POSITION = 2500
    
    print("\nGenerating disk scheduling scenario...")
    print(f"Disk cylinders: 0 - {NUM_CYLINDERS - 1}")
    print(f"Number of requests: {NUM_REQUESTS}")
    print(f"Initial head position: {INITIAL_POSITION}\n")
    
    # Create scheduler and run algorithms
    scheduler = DiskScheduler(NUM_CYLINDERS, NUM_REQUESTS, INITIAL_POSITION)
    results = scheduler.run_all_algorithms()
    
    # Print results
    print_results(scheduler, results)
    
    # Save all plots
    save_all_plots(scheduler, results)
    
    # Display plots
    print("\nDisplaying visualizations...")
    plt.show()


if __name__ == "__main__":
    main()
