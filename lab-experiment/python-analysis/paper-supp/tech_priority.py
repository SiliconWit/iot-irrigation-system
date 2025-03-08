import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class IrrigationContributionAnalyzer:
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
        
        # Efficiency factors for each technique
        self.technique_efficiency = {
            'IoT': 0.915,             # IoT alone provides about 8.5% savings vs traditional
            'Intercropping': 0.889,   # IoT+Intercropping provides about 11.1% more vs IoT alone
            'Drip': 0.850,            # Drip irrigation is about 15% more efficient
            'GravityPressure': 0.960  # Gravity pressure adds about 4% efficiency at 1.0m height
        }
        
        # Implementation factors
        self.implementation_factors = {
            'IoT': {'cost': 2.5, 'complexity': 8, 'maintenance': 7, 'scalability': 8},
            'Intercropping': {'cost': 1.2, 'complexity': 5, 'maintenance': 4, 'scalability': 7},
            'Drip': {'cost': 2.0, 'complexity': 6, 'maintenance': 5, 'scalability': 6},
            'GravityPressure': {'cost': 0.2, 'complexity': 1, 'maintenance': 1, 'scalability': 5}  # Additional over regular drip
        }

    def calculate_water_requirements(self):
        """Calculate water requirements for each irrigation system"""
        # Formula: Apply efficiency factors to calculate water requirements
        results = {}
        
        # 1. Traditional irrigation (baseline)
        trad_avg = np.mean([crop['total'] for crop in self.traditional_water.values() if crop != self.traditional_water['Rice']])
        results['Traditional'] = trad_avg
        
        # 2. IoT-controlled irrigation
        iot_avg = np.mean([crop['total'] for crop in self.iot_mono_water.values() if crop != self.iot_mono_water['Rice']])
        results['IoT'] = iot_avg
        
        # 3. IoT + Intercropping
        iot_intercrop_avg = np.mean([crop['total'] for crop in self.iot_intercrop_water.values()])
        results['IoT+Intercrop'] = iot_intercrop_avg
        
        # 4. IoT + Drip
        results['IoT+Drip'] = iot_avg * self.technique_efficiency['Drip']
        
        # 5. IoT + Intercrop + Drip
        results['IoT+Intercrop+Drip'] = iot_intercrop_avg * self.technique_efficiency['Drip']
        
        # 6. IoT + Intercrop + GravityDrip
        results['IoT+Intercrop+GravityDrip'] = (iot_intercrop_avg * 
                                             self.technique_efficiency['Drip'] * 
                                             self.technique_efficiency['GravityPressure'])
        
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
        savings['Drip'] = water_req['IoT+Intercrop'] - water_req['IoT+Intercrop+Drip']
        savings['GravityPressure'] = (water_req['IoT+Intercrop+Drip'] - 
                                   water_req['IoT+Intercrop+GravityDrip'])
        
        # Formula: Contribution_Percentage = (Savings_Technique / Total_Savings) * 100
        total_savings = baseline - water_req['IoT+Intercrop+GravityDrip']
        contribution = {tech: (saving / total_savings) * 100 for tech, saving in savings.items()}
            
        return contribution

    def calculate_system_savings(self):
        """Calculate total water savings for each system configuration"""
        # Formula: Savings_Percentage = ((Baseline - WR_System) / Baseline) * 100
        water_req = self.calculate_water_requirements()
        baseline = water_req['Traditional']
        
        system_savings = {system: ((baseline - requirement) / baseline) * 100 
                          for system, requirement in water_req.items()}
            
        return system_savings

    def calculate_implementation_priority(self):
        """Calculate implementation priority based on multiple factors"""
        # Formula: Priority = (Water_Savings / Cost) * (Scalability / (Complexity + Maintenance))
        contribution = self.calculate_savings_contribution()
        
        priority_scores = {}
        for technique, factors in self.implementation_factors.items():
            cost = factors['cost']
            complexity = factors['complexity']
            maintenance = factors['maintenance']
            scalability = factors['scalability']
            
            # Prevent division by zero
            cost = max(cost, 0.1)
            complexity_maintenance = max(complexity + maintenance, 0.1)
            
            # Calculate priority score
            if technique in contribution:
                priority_scores[technique] = (contribution[technique] / cost) * (scalability / complexity_maintenance)
        
        # Normalize scores
        max_score = max(priority_scores.values()) if priority_scores else 1
        priority_scores = {tech: (score / max_score) * 10 for tech, score in priority_scores.items()}
        
        # Sort by priority score
        sorted_priorities = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_priorities

    def create_implementation_roadmap(self):
        """Create implementation roadmap with water savings at each stage"""
        priorities = self.calculate_implementation_priority()
        priority_order = [p[0] for p in priorities]
        
        # Calculate water savings at each implementation phase
        water_req = self.calculate_water_requirements()
        baseline = water_req['Traditional']
        
        roadmap_data = []
        
        # Start with IoT as foundation
        roadmap_data.append({
            "Phase": 1,
            "Technique": "IoT System",
            "System": "IoT",
            "Water Req. (mm)": water_req["IoT"],
            "Total Savings (%)": ((baseline - water_req["IoT"]) / baseline) * 100,
            "Incremental Savings (%)": ((baseline - water_req["IoT"]) / baseline) * 100
        })
        
        # Add techniques in priority order
        phase = 2
        prev_system = "IoT"
        prev_savings = ((baseline - water_req["IoT"]) / baseline) * 100
        
        # Map of technique to next system name
        system_progression = {
            "IoT": {"Intercropping": "IoT+Intercrop", "Drip": "IoT+Drip"},
            "IoT+Intercrop": {"Drip": "IoT+Intercrop+Drip"},
            "IoT+Drip": {"Intercropping": "IoT+Intercrop+Drip"},
            "IoT+Intercrop+Drip": {"GravityPressure": "IoT+Intercrop+GravityDrip"}
        }
        
        for technique in priority_order:
            if technique == "IoT":
                continue  # Already added
                
            # Determine next system based on current system and technique
            if prev_system in system_progression and technique in system_progression[prev_system]:
                next_system = system_progression[prev_system][technique]
                
                if next_system in water_req:
                    total_savings = ((baseline - water_req[next_system]) / baseline) * 100
                    incremental = total_savings - prev_savings
                    
                    roadmap_data.append({
                        "Phase": phase,
                        "Technique": technique,
                        "System": next_system,
                        "Water Req. (mm)": water_req[next_system],
                        "Total Savings (%)": total_savings,
                        "Incremental Savings (%)": incremental
                    })
                    
                    prev_system = next_system
                    prev_savings = total_savings
                    phase += 1
        
        # Convert to DataFrame
        roadmap_df = pd.DataFrame(roadmap_data)
        roadmap_df = roadmap_df.round({"Water Req. (mm)": 3, "Total Savings (%)": 1, "Incremental Savings (%)": 1})
        
        return roadmap_df

    def plot_technique_contribution(self):
        """Plot the contribution of each technique to overall water savings"""
        contribution = self.calculate_savings_contribution()
        
        # Prepare data for plotting
        techniques = list(contribution.keys())
        contributions = list(contribution.values())
        
        # Sort by decreasing contribution
        sorted_indices = np.argsort(contributions)[::-1]
        sorted_techniques = [techniques[i] for i in sorted_indices]
        sorted_contributions = [contributions[i] for i in sorted_indices]
        
        # Create pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(sorted_contributions, labels=sorted_techniques, autopct='%1.1f%%',
                startangle=90, colors=plt.cm.tab10.colors)
        plt.axis('equal')
        plt.title('Contribution to Total Water Savings by Technique')
        
        return plt

    def plot_water_savings_by_system(self):
        """Plot water savings for each system configuration"""
        system_savings = self.calculate_system_savings()
        
        # Remove traditional (0% savings)
        if 'Traditional' in system_savings:
            del system_savings['Traditional']
        
        # Prepare data for plotting
        systems = list(system_savings.keys())
        savings = list(system_savings.values())
        
        # Sort by increasing savings
        sorted_indices = np.argsort(savings)
        sorted_systems = [systems[i] for i in sorted_indices]
        sorted_savings = [savings[i] for i in sorted_indices]
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        colors = plt.cm.YlGn(np.linspace(0.4, 0.8, len(sorted_systems)))
        bars = plt.barh(sorted_systems, sorted_savings, color=colors)
        
        # Add labels and values
        plt.xlabel('Water Savings (%)')
        plt.title('Water Savings by Irrigation System Configuration')
        
        # Add value labels to bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
                    ha='left', va='center')
        
        plt.tight_layout()
        return plt
        
    def plot_implementation_priorities(self):
        """Plot the implementation priorities of different techniques"""
        priorities = self.calculate_implementation_priority()
        
        # Prepare data for plotting
        techniques = [p[0] for p in priorities]
        scores = [p[1] for p in priorities]
        
        # Create horizontal bar chart
        plt.figure(figsize=(10, 5))
        
        # Use different colors for each bar
        colors = plt.cm.viridis(np.linspace(0, 0.8, len(techniques)))
        bars = plt.barh(techniques, scores, color=colors)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}',
                   ha='left', va='center')
        
        plt.xlabel('Priority Score (0-10)')
        plt.title('Implementation Priority by Technique')
        plt.tight_layout()
        
        return plt

    def generate_summary_tables(self):
        """Generate summary tables for water requirements, savings and priority"""
        # Water requirements table
        water_req = self.calculate_water_requirements()
        water_df = pd.DataFrame.from_dict(water_req, orient='index', columns=['Water Requirement (mm)'])
        water_df = water_df.round(3)
        
        # System savings table
        system_savings = self.calculate_system_savings()
        savings_df = pd.DataFrame.from_dict(system_savings, orient='index', columns=['Water Savings (%)'])
        savings_df = savings_df.round(1)
        
        # Technique contribution table
        contribution = self.calculate_savings_contribution()
        contrib_df = pd.DataFrame.from_dict(contribution, orient='index', columns=['Contribution to Total Savings (%)'])
        contrib_df = contrib_df.sort_values('Contribution to Total Savings (%)', ascending=False)
        contrib_df = contrib_df.round(1)
        
        # Implementation priority table
        priorities = self.calculate_implementation_priority()
        priority_df = pd.DataFrame(priorities, columns=['Technique', 'Priority Score'])
        priority_df = priority_df.set_index('Technique')
        priority_df = priority_df.round(1)
        
        return water_df, savings_df, contrib_df, priority_df

# Usage example
if __name__ == "__main__":
    analyzer = IrrigationContributionAnalyzer()
    
    # Generate implementation roadmap table
    roadmap = analyzer.create_implementation_roadmap()
    print("Implementation Roadmap with Water Savings:")
    print("="*80)
    print(roadmap.to_string(index=False))
    print("\n")
    
    # Generate summary tables
    water_df, savings_df, contrib_df, priority_df = analyzer.generate_summary_tables()
    
    print("Water Savings by Irrigation System:")
    print("="*50)
    print(savings_df.to_string())
    print("\n")
    
    print("Contribution of Each Technique to Total Water Savings:")
    print("="*50)
    print(contrib_df.to_string())
    print("\n")
    
    print("Implementation Priority Ranking:")
    print("="*50)
    print(priority_df.to_string())
    
    # Display system comparison plot
    print("\nGenerating system comparison plot...")
    system_plot = analyzer.plot_water_savings_by_system()
    
    # Display technique contribution plot
    print("Generating technique contribution plot...")
    contribution_plot = analyzer.plot_technique_contribution()
    
    # Display implementation priority plot
    print("Generating implementation priority plot...")
    priority_plot = analyzer.plot_implementation_priorities()
    
    # Show all plots
    plt.show()
