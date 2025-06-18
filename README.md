# WARN – Workforce Analytics & Recruitment Network

## Overview
Our project is a platform designed to connect recently laid-off tech employees with verified and promising startups. The platform leverages public layoff data and curated startup job listings to help recruiters and job seekers find the best opportunities quickly and efficiently.

## Features
- **Verified Startups Only:** Only trusted and high-potential startups are featured.
- **Layoff Data Access:** Recruiters can access detailed layoff data from major tech companies (e.g., Google, Apple, Meta), organized by region and time period.
- **Job Discovery:** Laid-off employees can browse startup job opportunities tailored to their skills and experience.
- **Data Visualizations:** Interactive visualizations such as tree maps highlight layoff trends and job market insights.
- **Predictive Insights:** Recruiters receive recommendations on optimal hiring times based on layoff cycles and market trends.
- **Premium Features:** Recruiters can pay to post jobs or directly contact talent; tech workers can sign up for enhanced job alerts.

## Data Sources
- **Layoff Data:** Sourced from public government WARN websites, providing up-to-date information on layoffs by company, region, and time period.
- **Startup Job Listings:** Scraped from Y Combinator’s job boards:
  - [Work at a Startup](https://www.workatastartup.com/jobs)
  - [Y Combinator Jobs](https://www.ycombinator.com/jobs)

## Visualizations
- **Tree Map:** Highlights the top five states with the largest number of tech layoffs, with section sizes proportional to layoff counts.
- **Seasonal Trends:** Showing in which months the most layoffs tend to happen.

## Getting Started
### Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/)

### Setup Instructions
1. **Clone the Repository:**
   ```powershell
   git clone <your-repo-url>
   cd fd2p
   ```
2. **Install Python Dependencies:**
   ```powershell
   cd ../python
   pip install -r requirements.txt
   ```
3. **Open in VS Code:**
   ```powershell
   code .
   ```

## Usage
- Run data processing scripts and visualizations from the `python/` directory.
- Place new data files in the `data/` directory.
- Refer to the code and documentation in the `python/` folder for details on available scripts and modules.

## Interactive Dashboard

The project includes an interactive dashboard for visualizing tech layoffs by state, company, and month using Plotly Dash.

### How to Run the Dashboard
1. Install the required dependencies (if not already installed):
   ```sh
   pip install -r python/requirements.txt
   ```
2. Run the dashboard application:
   ```sh
   python python/layoffs_dashboard.py
   ```
3. Open your browser and go to the address shown in the terminal (usually http://127.0.0.1:8050/).

### Dashboard Features
- **By State:** Treemap showing total layoffs in California, New York, Texas, and Washington.
- **By Company:** Treemap showing total layoffs by company across all states.
- **By Month:** Treemap showing total layoffs by month, aggregated from all states.

The dashboard provides interactive visualizations to help you explore layoff trends across different dimensions.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for suggestions or improvements.

## License
This project is licensed under the MIT License.

---

*For questions or support, please contact the project maintainer.*
