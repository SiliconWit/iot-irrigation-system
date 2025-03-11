import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import os

class IrrigationContributionAnalyzer:
    """
    Analyzes the contribution of different irrigation techniques to water savings
    and provides implementation recommendations for smallholder farmers.
    
    This class calculates water savings from various irrigation techniques:
    - IoT-controlled irrigation
    - Intercropping
    - Drip irrigation
    - Gravity-fed drip systems
    
    It also considers implementation factors such as cost, complexity,
    maintenance requirements, and scalability to provide prioritized
    recommendations for smallholder farmers.
    """
    def __init__(self):
        # Reference values for traditional irrigation (without IoT)
        self.traditional_water = {
            'Beans': {'initial': 9.084, 'development': 26.647, 'total': 35.732},
            'Maize': {'initial': 13.843, 'development': 23.533, 'total': 37.376},
            'Onions': {'initial': 12.978, 'development': 26.647, 'total': 39.625},
            'Rice': {'initial': 378.759, 'development': 0.000, 'total': 378.759}
        }
        
        # IoT-controlled irrigation measurements
        self.iot_mono_water = {
            'Beans': {'initial': 8.460, 'development': 24.210, 'total': 32.670},
            'Maize': {'initial': 12.750, 'development': 21.280, 'total': 34.030},
            'Onions': {'initial': 11.780, 'development': 24.510, 'total': 36.290},
            'Rice': {'initial': 346.180, 'development': 0.000, 'total': 346.180}
        }
        
        # IoT + Intercropping measured values
        self.iot_intercrop_water = {
            'Maize+Beans': {'initial': 10.194, 'development': 19.476, 'total': 29.670},
            'Onions+Beans': {'initial': 9.713, 'development': 20.736, 'total': 30.449},
            'Maize+Onions': {'initial': 11.738, 'development': 19.405, 'total': 31.143}
        }
        
        # Gravity drip measurements at 2.5m head
        self.gravity_drip_water = {
            'Beans': {'initial': 6.599, 'development': 18.884, 'total': 25.483},
            'Maize': {'initial': 9.945, 'development': 16.598, 'total': 26.543},
            'Onions': {'initial': 9.188, 'development': 19.118, 'total': 28.306}
        }
        
        # Gravity drip intercropping measurements at 2.5m head
        self.gravity_drip_intercrop = {
            'Maize+Beans': {'initial': 7.951, 'development': 15.191, 'total': 23.143},
            'Onions+Beans': {'initial': 7.576, 'development': 16.174, 'total': 23.750},
            'Maize+Onions': {'initial': 9.156, 'development': 15.136, 'total': 24.292}
        }
        
        # Updated efficiency factors based on the provided screenshots
        self.technique_efficiency = {
            'IoT': 0.91,              # IoT alone provides about 9% savings vs traditional
            'Intercropping': 0.89,    # Intercropping provides about 11% savings on top of IoT
            'Drip': 0.78,             # Drip irrigation provides about 22% savings
            'GravityPressure': {      # Different operating heads provide different efficiency
                '1.0m': 0.973,        # 27.0% total savings vs standard intercropping at 1.0m
                '2.5m': 0.964,        # 30.6% total savings vs standard intercropping at 2.5m
                '3.5m': 0.962,        # 31.5% total savings vs standard intercropping at 3.5m
                '4.5m': 0.960,        # 32.4% total savings vs standard intercropping at 4.5m
                '5.5m': 0.958         # 33.3% total savings vs standard intercropping at 5.5m
            }
        }
        
        # Implementation factors for smallholder farmers
        # (1-10 scale, with lower is better for cost, complexity, maintenance)
        self.implementation_factors = {
            'Traditional': {'cost': 1.0, 'complexity': 2, 'maintenance': 3, 'scalability': 3},
            'IoT': {'cost': 8.5, 'complexity': 8, 'maintenance': 7, 'scalability': 6},
            'Intercropping': {'cost': 2.0, 'complexity': 5, 'maintenance': 4, 'scalability': 7},
            'Drip': {'cost': 6.0, 'complexity': 6, 'maintenance': 5, 'scalability': 5},
            'GravityDrip': {'cost': 3.5, 'complexity': 4, 'maintenance': 3, 'scalability': 4}
        }
        
        # Resource constraints for smallholder farmers
        self.resource_constraints = {
            'capital': 'low',      # Limited financial resources
            'technical_skill': 'moderate',  # Some technical capability but limited
            'labor': 'high',       # Labor availability is relatively high
            'water_access': 'limited',     # Limited water resources
            'education': 'moderate'        # Some educational capacity
        }

    def calculate_water_requirements(self):
        """Calculate water requirements for each irrigation system, based on actual data"""
        results = {}
        
        # 1. Traditional irrigation (baseline)
        # Calculate average water requirement for traditional monoculture
        # (excluding rice which is an outlier)
        trad_values = [values['total'] for crop, values in self.traditional_water.items() if crop != 'Rice']
        results['Traditional'] = np.mean(trad_values)
        
        # 2. IoT-controlled irrigation
        # Calculate average water requirement for IoT monoculture
        # (excluding rice which is an outlier)
        iot_values = [values['total'] for crop, values in self.iot_mono_water.items() if crop != 'Rice']
        results['IoT'] = np.mean(iot_values)
        
        # 3. IoT + Intercropping
        # Calculate average water requirement for IoT intercropping
        intercrop_values = [values['total'] for values in self.iot_intercrop_water.values()]
        results['IoT+Intercrop'] = np.mean(intercrop_values)
        
        # 4. IoT + Gravity-fed Drip
        # Calculate average water requirement for gravity-fed drip irrigation
        # (excluding rice which is an outlier)
        drip_values = [values['total'] for crop, values in self.gravity_drip_water.items()]
        results['IoT+GravityDrip'] = np.mean(drip_values)
        
        # 5. IoT + Intercrop + Gravity-fed Drip
        # Calculate average water requirement for gravity-fed drip irrigation with intercropping
        gravity_intercrop_values = [values['total'] for values in self.gravity_drip_intercrop.values()]
        results['IoT+Intercrop+GravityDrip'] = np.mean(gravity_intercrop_values)
        
        return results

    def calculate_savings_contribution(self):
        """Calculate how much each technique contributes to overall water savings"""
        # Formula: Savings_Technique = WR_Previous - WR_WithTechnique
        water_req = self.calculate_water_requirements()
        baseline = water_req['Traditional']
        
        # Calculate absolute water savings for each technique
        savings = {}
        savings['IoT'] = baseline - water_req['IoT']
        savings['Intercropping'] = water_req['IoT'] - water_req['IoT+Intercrop']
        
        # Contribution from gravity-fed drip depends on whether it's applied to monoculture or intercropping
        savings['GravityDrip_mono'] = water_req['IoT'] - water_req['IoT+GravityDrip']
        savings['GravityDrip_intercrop'] = water_req['IoT+Intercrop'] - water_req['IoT+Intercrop+GravityDrip']
        
        # Formula: Contribution_Percentage = (Savings_Technique / Total_Savings) * 100
        total_savings = baseline - water_req['IoT+Intercrop+GravityDrip']
        
        # Calculate contribution percentage
        contribution = {}
        for tech, saving in savings.items():
            contribution[tech] = (saving / total_savings) * 100
            
        return contribution, savings, total_savings

    def calculate_system_savings(self):
        """Calculate total water savings for each system configuration"""
        # Formula: Savings_Percentage = ((Baseline - WR_System) / Baseline) * 100
        water_req = self.calculate_water_requirements()
        baseline = water_req['Traditional']
        
        system_savings = {system: ((baseline - requirement) / baseline) * 100 
                          for system, requirement in water_req.items()}
            
        return system_savings

    def calculate_benefit_cost_ratio(self):
        """Calculate benefit-to-cost ratio for each technique"""
        # Get contribution data
        contribution, savings, _ = self.calculate_savings_contribution()
        
        # Calculate benefit-cost ratio
        # Higher ratios mean better value for the investment
        benefit_cost = {}
        
        # IoT system
        iot_cost = self.implementation_factors['IoT']['cost']
        iot_benefit = contribution['IoT']
        benefit_cost['IoT'] = iot_benefit / iot_cost
        
        # Intercropping
        intercrop_cost = self.implementation_factors['Intercropping']['cost']
        intercrop_benefit = contribution['Intercropping']
        benefit_cost['Intercropping'] = intercrop_benefit / intercrop_cost
        
        # Gravity-fed drip for intercropping systems
        gravity_cost = self.implementation_factors['GravityDrip']['cost']
        gravity_benefit = contribution['GravityDrip_intercrop']
        benefit_cost['GravityDrip'] = gravity_benefit / gravity_cost
        
        return benefit_cost

    def calculate_implementation_complexity(self):
        """Calculate overall implementation complexity for each technique"""
        complexity = {}
        
        for tech, factors in self.implementation_factors.items():
            # Skip traditional as a baseline
            if tech == 'Traditional':
                continue
                
            # Complexity formula: (complexity + maintenance) / scalability
            # Lower values are better (less complex per unit of scalability)
            complexity[tech] = (factors['complexity'] + factors['maintenance']) / factors['scalability']
            
        return complexity

    def calculate_implementation_priority(self):
        """Calculate implementation priority based on multiple factors for smallholder farmers"""
        # Get benefit-cost ratio
        benefit_cost = self.calculate_benefit_cost_ratio()
        
        # Get implementation complexity
        complexity = self.calculate_implementation_complexity()
        
        # Calculate priority score
        # Formula: Priority = (Benefit/Cost) / Complexity
        # Higher is better
        priority_scores = {}
        
        for tech in benefit_cost:
            if tech in complexity:
                priority_scores[tech] = benefit_cost[tech] / complexity[tech]
        
        # Normalize scores for easier interpretation (0-10 scale)
        max_score = max(priority_scores.values()) if priority_scores else 1
        priority_scores = {tech: (score / max_score) * 10 for tech, score in priority_scores.items()}
        
        # Sort by priority score
        sorted_priorities = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_priorities

    def create_implementation_roadmap(self):
        """Create a step-by-step implementation roadmap specifically for smallholder farmers"""
        priorities = self.calculate_implementation_priority()
        priority_order = [p[0] for p in priorities]
        
        # Calculate water savings at each implementation phase
        water_req = self.calculate_water_requirements()
        baseline = water_req['Traditional']
        
        roadmap_data = []
        
        # Start with Traditional as baseline
        roadmap_data.append({
            "Phase": 0,
            "Technique": "Traditional Irrigation",
            "System": "Traditional",
            "Water Req. (mm)": water_req["Traditional"],
            "Total Savings (%)": 0.0,
            "Incremental Savings (%)": 0.0,
            "Implementation Cost": self.implementation_factors["Traditional"]["cost"],
            "Technical Complexity": self.implementation_factors["Traditional"]["complexity"]
        })
        
        # Add techniques in priority order
        phase = 1
        prev_system = "Traditional"
        prev_savings = 0.0
        
        # Map of technique to next system name and technique progression
        system_progression = {
            "Traditional": {
                "Intercropping": "Intercrop", 
                "IoT": "IoT", 
                "GravityDrip": "GravityDrip"
            },
            "Intercrop": {
                "IoT": "IoT+Intercrop", 
                "GravityDrip": "Intercrop+GravityDrip"
            },
            "IoT": {
                "Intercropping": "IoT+Intercrop", 
                "GravityDrip": "IoT+GravityDrip"
            },
            "GravityDrip": {
                "IoT": "IoT+GravityDrip", 
                "Intercropping": "Intercrop+GravityDrip"
            },
            "IoT+Intercrop": {
                "GravityDrip": "IoT+Intercrop+GravityDrip"
            },
            "Intercrop+GravityDrip": {
                "IoT": "IoT+Intercrop+GravityDrip"
            },
            "IoT+GravityDrip": {
                "Intercropping": "IoT+Intercrop+GravityDrip"
            }
        }
        
        # We need custom water requirements for combinations not in original data
        custom_systems = {
            "Intercrop": baseline * 0.94,  # Intercropping alone saves about 6%
            "Intercrop+GravityDrip": baseline * 0.72,  # Combined savings of about 28%
            "GravityDrip": baseline * 0.82  # Gravity drip alone saves about 18%
        }
        
        # Add the custom systems to water_req
        for system, value in custom_systems.items():
            if system not in water_req:
                water_req[system] = value
        
        # Follow the priority order to create the roadmap
        for technique in priority_order:
            if prev_system in system_progression and technique in system_progression[prev_system]:
                next_system = system_progression[prev_system][technique]
                
                # Calculate water requirement and savings
                if next_system in water_req:
                    next_req = water_req[next_system]
                else:
                    # If we don't have data, estimate it based on efficiency factors
                    # This is a fallback but shouldn't be needed with our current data
                    next_req = water_req[prev_system] * 0.9  # Assume 10% additional savings
                
                total_savings = ((baseline - next_req) / baseline) * 100
                incremental = total_savings - prev_savings
                
                roadmap_data.append({
                    "Phase": phase,
                    "Technique": technique,
                    "System": next_system,
                    "Water Req. (mm)": next_req,
                    "Total Savings (%)": total_savings,
                    "Incremental Savings (%)": incremental,
                    "Implementation Cost": self.implementation_factors[technique]["cost"],
                    "Technical Complexity": self.implementation_factors[technique]["complexity"]
                })
                
                prev_system = next_system
                prev_savings = total_savings
                phase += 1
        
        # Convert to DataFrame
        roadmap_df = pd.DataFrame(roadmap_data)
        roadmap_df = roadmap_df.round({
            "Water Req. (mm)": 2, 
            "Total Savings (%)": 1, 
            "Incremental Savings (%)": 1
        })
        
        return roadmap_df

    def plot_technique_contribution(self, save_path=None):
        """Plot the contribution of each technique to overall water savings"""
        contribution, _, _ = self.calculate_savings_contribution()
        
        # Clean up the keys for the pie chart
        cleaned_contribution = {
            'IoT System': contribution['IoT'],
            'Intercropping': contribution['Intercropping'],
            'Gravity-Fed Drip': contribution['GravityDrip_intercrop']
        }
        
        # Prepare data for plotting
        techniques = list(cleaned_contribution.keys())
        contributions = list(cleaned_contribution.values())
        
        # Sort by decreasing contribution
        sorted_indices = np.argsort(contributions)[::-1]
        sorted_techniques = [techniques[i] for i in sorted_indices]
        sorted_contributions = [contributions[i] for i in sorted_indices]
        
        # Create color map - use agriculturally relevant colors
        colors = ['#3A7D44', '#6CB28E', '#81C3D7']  # Green, light green, blue
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        patches, texts, autotexts = plt.pie(
            sorted_contributions, 
            labels=sorted_techniques, 
            autopct='%1.1f%%',
            startangle=90, 
            colors=colors,
            shadow=True
        )
        
        # Enhance text visibility
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        plt.axis('equal')
        plt.title('Contribution to Total Water Savings by Irrigation Technique', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return plt

    def plot_water_savings_by_system(self, save_path=None):
        """Plot water savings for each system configuration"""
        system_savings = self.calculate_system_savings()
        
        # Remove traditional (0% savings)
        if 'Traditional' in system_savings:
            del system_savings['Traditional']
        
        # Create more readable system names
        system_display_names = {
            'IoT': 'IoT System Only',
            'IoT+Intercrop': 'IoT + Intercropping',
            'IoT+GravityDrip': 'IoT + Gravity-Fed Drip',
            'IoT+Intercrop+GravityDrip': 'IoT + Intercropping + Gravity-Fed Drip'
        }
        
        # Replace keys with display names
        renamed_savings = {system_display_names.get(k, k): v for k, v in system_savings.items()}
        
        # Prepare data for plotting
        systems = list(renamed_savings.keys())
        savings = list(renamed_savings.values())
        
        # Sort by increasing savings
        sorted_indices = np.argsort(savings)
        sorted_systems = [systems[i] for i in sorted_indices]
        sorted_savings = [savings[i] for i in sorted_indices]
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Use a color gradient from light to dark green
        colors = plt.cm.YlGn(np.linspace(0.4, 0.8, len(sorted_systems)))
        bars = plt.barh(sorted_systems, sorted_savings, color=colors)
        
        # Add labels and values
        plt.xlabel('Water Savings (%)', fontsize=14)
        plt.title('Water Savings by Irrigation System Configuration', fontsize=16, fontweight='bold')
        
        # Add value labels to bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
                    ha='left', va='center', fontsize=12, fontweight='bold')
        
        # Add grid lines for better readability
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return plt
        
    def plot_implementation_priorities(self, save_path=None):
        """Plot the implementation priorities of different techniques"""
        priorities = self.calculate_implementation_priority()
        
        # Create more readable technique names
        technique_display_names = {
            'Intercropping': 'Intercropping',
            'GravityDrip': 'Gravity-Fed Drip Irrigation',
            'IoT': 'IoT-Controlled Irrigation'
        }
        
        # Replace with display names
        priorities = [(technique_display_names.get(t, t), score) for t, score in priorities]
        
        # Prepare data for plotting
        techniques = [p[0] for p in priorities]
        scores = [p[1] for p in priorities]
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 7))
        
        # Use a green-blue color palette
        colors = ['#2D6A4F', '#40916C', '#52B788'][:len(techniques)]
        bars = plt.barh(techniques, scores, color=colors)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}',
                   ha='left', va='center', fontsize=12, fontweight='bold')
        
        # Add decorative elements and labels
        plt.xlabel('Implementation Priority Score (0-10)', fontsize=14)
        plt.title('Irrigation Technique Implementation Priority for Smallholder Farmers', 
                 fontsize=16, fontweight='bold')
        
        # Add grid lines
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add explanatory annotation
        plt.annotate('Higher scores indicate higher priority based on\nwater savings, cost, complexity, and scalability',
                    xy=(0.98, 0.02), xycoords='axes fraction',
                    ha='right', va='bottom',
                    bbox=dict(boxstyle="round,pad=0.3", fc="#F8F9FA", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return plt

    def plot_benefit_cost_comparison(self, save_path=None):
        """Plot benefit-cost ratio for each technique"""
        benefit_cost = self.calculate_benefit_cost_ratio()
        
        # Create more readable technique names
        technique_display_names = {
            'Intercropping': 'Intercropping',
            'GravityDrip': 'Gravity-Fed Drip',
            'IoT': 'IoT System'
        }
        
        # Replace with display names
        renamed_bc = {technique_display_names.get(k, k): v for k, v in benefit_cost.items()}
        
        # Sort by decreasing benefit-cost ratio
        sorted_bc = sorted(renamed_bc.items(), key=lambda x: x[1], reverse=True)
        techniques = [item[0] for item in sorted_bc]
        bc_ratios = [item[1] for item in sorted_bc]
        
        # Create the figure
        plt.figure(figsize=(12, 8))
        
        # Use a distinct color palette
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(techniques)))
        bars = plt.bar(techniques, bc_ratios, color=colors, width=0.6)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Add labels and title
        plt.ylabel('Benefit-Cost Ratio', fontsize=14)
        plt.title('Benefit-Cost Ratio by Irrigation Technique for Smallholder Farmers',
                 fontsize=16, fontweight='bold')
        plt.ylim(0, max(bc_ratios) * 1.15)  # Add space for labels
        
        # Add grid lines
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add explanatory annotation
        plt.annotate('Higher values indicate better return on investment',
                    xy=(0.98, 0.02), xycoords='axes fraction',
                    ha='right', va='bottom',
                    bbox=dict(boxstyle="round,pad=0.3", fc="#F8F9FA", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        return plt

    def plot_roadmap_visualization(self, save_path=None):
        """Create a visual representation of the implementation roadmap"""
        roadmap = self.create_implementation_roadmap()
        
        # Create the figure
        fig, ax1 = plt.subplots(figsize=(14, 10))
        
        # Get data for plotting
        phases = roadmap['Phase'].tolist()
        techniques = roadmap['Technique'].tolist()
        water_req = roadmap['Water Req. (mm)'].tolist()
        savings = roadmap['Total Savings (%)'].tolist()
        
        # Calculate positions for the techniques
        x_pos = np.arange(len(phases))
        
        # Create bar chart for water requirements
        bars = ax1.bar(x_pos, water_req, width=0.6, 
                      color=plt.cm.Blues(np.linspace(0.3, 0.8, len(phases))))
        
        # Add a second y-axis for water savings
        ax2 = ax1.twinx()
        line = ax2.plot(x_pos, savings, 'ro-', linewidth=3, markersize=10)
        
        # Set axis labels and title
        ax1.set_xlabel('Implementation Phase', fontsize=14)
        ax1.set_ylabel('Water Requirement (mm)', fontsize=14, color='blue')
        ax2.set_ylabel('Total Water Savings (%)', fontsize=14, color='red')
        
        # Set tick labels to the techniques
        plt.xticks(x_pos, techniques, rotation=45, ha='right')
        
        # Set y-axis formats
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.yaxis.set_major_formatter(PercentFormatter())
        
        # Add value labels to bars and line
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom')
            
            # Add savings labels
            if i > 0:  # Skip the first point (no savings)
                ax2.text(x_pos[i], savings[i] + 1, f'{savings[i]:.1f}%',
                        ha='center', va='bottom', color='red', fontweight='bold')
        
        # Add title
        plt.title('Implementation Roadmap for Smallholder Farmers', fontsize=16, fontweight='bold')
        
        # Add explanatory annotation
        plt.annotate('Recommended progression showing water requirements and cumulative savings',
                    xy=(0.98, 0.02), xycoords='axes fraction',
                    ha='right', va='bottom',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        return plt

    def plot_complexity_cost_matrix(self, save_path=None):
        """Create a complexity-cost matrix for the different techniques"""
        # Extract complexity and cost data
        techniques = ['Intercropping', 'GravityDrip', 'IoT']
        
        # Create more readable technique names
        technique_display_names = {
            'Intercropping': 'Intercropping',
            'GravityDrip': 'Gravity-Fed Drip',
            'IoT': 'IoT System',
            'Traditional': 'Traditional'
        }
        
        # Get costs and complexity values
        costs = [self.implementation_factors[t]['cost'] for t in techniques]
        complexity = [self.implementation_factors[t]['complexity'] for t in techniques]
        
        # Create a DataFrame for easier plotting
        df = pd.DataFrame({
            'Technique': [technique_display_names[t] for t in techniques],
            'Cost': costs,
            'Complexity': complexity
        })
        
        # Create the scatter plot
        plt.figure(figsize=(12, 9))
        
        # Define the size of each point based on water savings contribution
        contribution, _, _ = self.calculate_savings_contribution()
        sizes = []
        for t in techniques:
            if t == 'GravityDrip':
                # Use the intercrop variant
                sizes.append(contribution['GravityDrip_intercrop'] * 10)
            else:
                sizes.append(contribution[t] * 10)
        
        # Create the scatter plot
        scatter = plt.scatter(
            df['Cost'], 
            df['Complexity'], 
            s=sizes, 
            c=range(len(df)), 
            cmap='viridis', 
            alpha=0.7
        )
        
        # Add labels for each point
        for i, row in df.iterrows():
            plt.annotate(
                row['Technique'], 
                (row['Cost'], row['Complexity']), 
                xytext=(7, 0), 
                textcoords='offset points',
                fontsize=12,
                fontweight='bold'
            )
        
        # Add traditional irrigation as a reference point
        trad_cost = self.implementation_factors['Traditional']['cost']
        trad_complexity = self.implementation_factors['Traditional']['complexity']
        plt.scatter(trad_cost, trad_complexity, s=50, c='red', marker='x')
        plt.annotate(
            'Traditional', 
            (trad_cost, trad_complexity), 
            xytext=(7, 0), 
            textcoords='offset points',
            fontsize=12,
            color='red'
        )
        
        # Add explanatory elements
        plt.title('Implementation Cost vs. Complexity Matrix', fontsize=16, fontweight='bold')
        plt.xlabel('Cost (1-10 scale)', fontsize=14)
        plt.ylabel('Technical Complexity (1-10 scale)', fontsize=14)
        
        # Add a colorbar legend
        cbar = plt.colorbar(scatter)
        cbar.set_label('Priority Order', fontsize=12)
        
        # Add size legend explaining the bubble sizes
        plt.annotate(
            'Bubble size represents water savings contribution',
            xy=(0.02, 0.02), 
            xycoords='axes fraction',
            ha='left', 
            va='bottom',
            bbox=dict(boxstyle="round,pad=0.3", fc="#F8F9FA", ec="gray", alpha=0.8)
        )
        
        # Add quadrant labels
        plt.axhline(y=5, color='gray', linestyle='--', alpha=0.5)
        plt.axvline(x=5, color='gray', linestyle='--', alpha=0.5)
        
        # Add quadrant annotations
        quadrants = [
            {'pos': (2.5, 2.5), 'text': 'Low Cost\nLow Complexity\n(IDEAL)'},
            {'pos': (7.5, 2.5), 'text': 'High Cost\nLow Complexity'},
            {'pos': (2.5, 7.5), 'text': 'Low Cost\nHigh Complexity'},
            {'pos': (7.5, 7.5), 'text': 'High Cost\nHigh Complexity\n(CHALLENGING)'}
        ]
        
        for q in quadrants:
            plt.annotate(
                q['text'],
                xy=q['pos'],
                ha='center',
                va='center',
                fontsize=9,
                alpha=0.7,
                bbox=dict(boxstyle="round,pad=0.3", fc="#F8F9FA", ec="gray", alpha=0.3)
            )
        
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        return plt

    def plot_operating_head_impact(self, save_path=None):
        """Plot the impact of different operating heads on water savings"""
        # Extract data from efficiency factors
        heads = []
        savings = []
        
        for head, factor in self.technique_efficiency['GravityPressure'].items():
            heads.append(head)
            # Convert efficiency factor to water savings percentage
            intercrop_baseline = 11.0  # Base water savings from intercropping
            savings_value = (1 - factor) * 100 + intercrop_baseline
            savings.append(savings_value)
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Create a gradient color palette
        colors = plt.cm.Blues(np.linspace(0.5, 0.9, len(heads)))
        
        # Create the bar chart
        bars = plt.bar(heads, savings, color=colors, width=0.6)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Customize the plot
        plt.title('Effect of Operating Head on Water Savings\n(Maize + Beans with Gravity-Fed Drip)', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Operating Head Height', fontsize=14)
        plt.ylabel('Total Water Savings (%)', fontsize=14)
        
        # Add a horizontal line at the optimal operating head (2.5m)
        optimal_head = '2.5m'
        optimal_savings = next((s for h, s in zip(heads, savings) if h == optimal_head), None)
        
        if optimal_savings:
            plt.axhline(y=optimal_savings, xmin=0.2, xmax=0.4, color='red', linestyle='--')
            
            # Add annotation for recommended operating head
            plt.annotate('Recommended operating head\n(optimal balance of performance & practicality)', 
                        xy=(heads.index(optimal_head), optimal_savings), 
                        xytext=(20, -20),
                        textcoords="offset points",
                        ha='left', va='top',
                        color='red', fontweight='bold',
                        arrowprops=dict(arrowstyle="->", color='red'))
        
        # Add grid lines
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # FIX: Set y-axis limits properly to show the data
        plt.ylim(12, 16)  # Set y-axis range to properly show the values (13.7% to 15.2%)
        
        # Add custom tick marks for better readability
        plt.yticks(np.arange(13, 16, 0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return plt

    def generate_summary_tables(self):
        """Generate summary tables for water requirements, savings and priority"""
        # Water requirements table
        water_req = self.calculate_water_requirements()
        water_df = pd.DataFrame.from_dict(water_req, orient='index', columns=['Water Requirement (mm)'])
        water_df = water_df.round(2)
        
        # System savings table
        system_savings = self.calculate_system_savings()
        savings_df = pd.DataFrame.from_dict(system_savings, orient='index', columns=['Water Savings (%)'])
        savings_df = savings_df.round(1)
        
        # Technique contribution table
        contribution, _, _ = self.calculate_savings_contribution()
        # Clean up the contribution data to remove sub-categories
        cleaned_contrib = {
            'IoT': contribution['IoT'],
            'Intercropping': contribution['Intercropping'],
            'Gravity-Fed Drip': contribution['GravityDrip_intercrop']
        }
        contrib_df = pd.DataFrame.from_dict(cleaned_contrib, orient='index', columns=['Contribution to Total Savings (%)'])
        contrib_df = contrib_df.sort_values('Contribution to Total Savings (%)', ascending=False)
        contrib_df = contrib_df.round(1)
        
        # Benefit-cost ratio table
        benefit_cost = self.calculate_benefit_cost_ratio()
        # Rename GravityDrip key
        if 'GravityDrip' in benefit_cost:
            benefit_cost['Gravity-Fed Drip'] = benefit_cost.pop('GravityDrip')
        bc_df = pd.DataFrame.from_dict(benefit_cost, orient='index', columns=['Benefit-Cost Ratio'])
        bc_df = bc_df.sort_values('Benefit-Cost Ratio', ascending=False)
        bc_df = bc_df.round(2)
        
        # Implementation priority table
        priorities = self.calculate_implementation_priority()
        # Create more readable names for display
        clean_priorities = []
        for tech, score in priorities:
            if tech == 'GravityDrip':
                clean_priorities.append(('Gravity-Fed Drip', score))
            else:
                clean_priorities.append((tech, score))
                
        priority_df = pd.DataFrame(clean_priorities, columns=['Technique', 'Priority Score'])
        priority_df = priority_df.set_index('Technique')
        priority_df = priority_df.round(1)
        
        return water_df, savings_df, contrib_df, bc_df, priority_df
    
    def generate_smallholder_recommendations(self):
        """Generate specific recommendations for smallholder farmers"""
        # Get key data
        priorities = self.calculate_implementation_priority()
        roadmap = self.create_implementation_roadmap()
        
        # Extract the top priority technique
        top_technique = priorities[0][0]
        
        # Simplify technique names for display
        technique_names = {
            'IoT': 'IoT-controlled irrigation',
            'Intercropping': 'intercropping',
            'GravityDrip': 'gravity-fed drip irrigation'
        }
        
        # Format the recommendation based on priorities
        recommendations = {
            'top_priority': technique_names.get(top_technique, top_technique),
            'implementation_order': [technique_names.get(tech, tech) for tech, _ in priorities],
            'immediate_step': roadmap.iloc[1]['Technique'] if len(roadmap) > 1 else None,
            'expected_savings': roadmap.iloc[1]['Incremental Savings (%)'] if len(roadmap) > 1 else 0,
            'long_term_target': roadmap.iloc[-1]['System'] if len(roadmap) > 0 else None,
            'maximum_savings': roadmap.iloc[-1]['Total Savings (%)'] if len(roadmap) > 0 else 0
        }
        
        return recommendations
    
    def generate_all_plots(self, output_dir='plots'):
        """Generate all plots and save them as PDF files"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all plots
        plots = {
            'water_savings': self.plot_water_savings_by_system(os.path.join(output_dir, 'water_savings.pdf')),
            'technique_contribution': self.plot_technique_contribution(os.path.join(output_dir, 'technique_contribution.pdf')),
            'implementation_priorities': self.plot_implementation_priorities(os.path.join(output_dir, 'implementation_priorities.pdf')),
            'benefit_cost': self.plot_benefit_cost_comparison(os.path.join(output_dir, 'benefit_cost.pdf')),
            'roadmap': self.plot_roadmap_visualization(os.path.join(output_dir, 'implementation_roadmap.pdf')),
            'complexity_cost': self.plot_complexity_cost_matrix(os.path.join(output_dir, 'complexity_cost.pdf')),
            'operating_head': self.plot_operating_head_impact(os.path.join(output_dir, 'operating_head.pdf'))
        }
        
        return plots
    
    def run_full_analysis(self, output_dir='results'):
        """Run a complete analysis and save all results"""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        plots_dir = os.path.join(output_dir, 'plots')
        
        # Generate all plots
        self.generate_all_plots(plots_dir)
        
        # Generate summary tables
        water_df, savings_df, contrib_df, bc_df, priority_df = self.generate_summary_tables()
        
        # Generate implementation roadmap
        roadmap_df = self.create_implementation_roadmap()
        
        # Generate recommendations
        recommendations = self.generate_smallholder_recommendations()
        
        # Save tables to CSV
        water_df.to_csv(os.path.join(output_dir, 'water_requirements.csv'))
        savings_df.to_csv(os.path.join(output_dir, 'water_savings.csv'))
        contrib_df.to_csv(os.path.join(output_dir, 'technique_contribution.csv'))
        bc_df.to_csv(os.path.join(output_dir, 'benefit_cost.csv'))
        priority_df.to_csv(os.path.join(output_dir, 'implementation_priority.csv'))
        roadmap_df.to_csv(os.path.join(output_dir, 'implementation_roadmap.csv'), index=False)
        
        # Return summary of all results
        return {
            'water_requirements': water_df,
            'water_savings': savings_df,
            'technique_contribution': contrib_df,
            'benefit_cost': bc_df,
            'implementation_priority': priority_df,
            'implementation_roadmap': roadmap_df,
            'recommendations': recommendations
        }

# Example usage
if __name__ == "__main__":
    # Create the analyzer
    analyzer = IrrigationContributionAnalyzer()
    
    # Run complete analysis
    results = analyzer.run_full_analysis()
    
    # Print key findings
    print("\n=== IRRIGATION STRATEGY ANALYSIS FOR SMALLHOLDER FARMERS ===\n")
    
    print("Water Savings by Irrigation System:")
    print("-"*60)
    print(results['water_savings'].to_string())
    print("\n")
    
    print("Contribution of Each Technique to Total Water Savings:")
    print("-"*60)
    print(results['technique_contribution'].to_string())
    print("\n")
    
    print("Benefit-Cost Analysis:")
    print("-"*60)
    print(results['benefit_cost'].to_string())
    print("\n")
    
    print("Implementation Priority Ranking:")
    print("-"*60)
    print(results['implementation_priority'].to_string())
    print("\n")
    
    print("Implementation Roadmap:")
    print("-"*60)
    print(results['implementation_roadmap'].to_string())
    print("\n")
    
    print("Recommendations for Smallholder Farmers:")
    print("-"*60)
    recs = results['recommendations']
    print(f"1. Top priority technique: {recs['top_priority']}")
    print(f"2. Recommended implementation order: {' → '.join(recs['implementation_order'])}")
    print(f"3. Immediate next step: Implement {recs['immediate_step']}")
    print(f"4. Expected immediate water savings: {recs['expected_savings']:.1f}%")
    print(f"5. Long-term target system: {recs['long_term_target']}")
    print(f"6. Maximum potential water savings: {recs['maximum_savings']:.1f}%")
    print("\n")
    
    print("All results have been saved to the 'results' directory.")
    print("Visualization plots have been saved to the 'results/plots' directory.")