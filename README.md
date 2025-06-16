# From Data to Product

## Overview
Our project is a platform designed to connect recently laid-off tech employees with verified and promising startups. The platform leverages public layoff data and curated startup job listings to help recruiters and job seekers find the best opportunities quickly and efficiently.

## Features
- **Verified Startups Only:** Only trusted and high-potential startups are featured.
- **Layoff Data Access:** Recruiters can access detailed layoff data from major tech companies (e.g., Google, Apple, Meta), organized by region and time period.
- **Job Discovery:** Laid-off employees can browse startup job opportunities tailored to their skills and experience.
- **Data Visualizations:** Interactive visualizations such as tree maps and heat maps highlight layoff trends and job market insights.
- **Predictive Insights:** Recruiters receive recommendations on optimal hiring times based on layoff cycles and market trends.
- **Premium Features:** Recruiters can pay to post jobs or directly contact talent; tech workers can sign up for enhanced job alerts.

## Data Sources
- **Layoff Data:** Sourced from public government WARN websites, providing up-to-date information on layoffs by company, region, and time period.
- **Startup Job Listings:** Scraped from Y Combinator’s job boards:
  - [Work at a Startup](https://www.workatastartup.com/jobs)
  - [Y Combinator Jobs](https://www.ycombinator.com/jobs)
- **Job Position Mapping:** Company and location data from WARN notices are linked with public job postings (e.g., LinkedIn) to analyze roles affected by layoffs.

## Visualizations
- **Tree Map:** Highlights the top five states with the largest number of tech layoffs, with section sizes proportional to layoff counts.
- **Heat Map:** Displays job roles (columns) against companies or states (rows) to visualize layoff patterns by position and location.

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

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for suggestions or improvements.

## License
This project is licensed under the MIT License.

---

*For questions or support, please contact the project maintainer.*
