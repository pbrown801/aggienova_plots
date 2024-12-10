# Aggienova Plots

An interactive Next.js web application for visualizing and analyzing supernova photometry data from the Aggienova project. This tool enables researchers and astronomy enthusiasts to explore and compare light curves across different supernovae and filter bands.

[![Visit Website](https://img.shields.io/badge/Visit-Website-blue)](https://aggienova-plots.vercel.app/)

## 🚀 Features

### Data Exploration
- **Supernova Search**: Easily search and plot data for specific supernovae by name
- **Type-based Analysis**: Plot and compare all supernovae of a specific classification
- **Multi-filter Support**: View data across various photometric filters (U, V, B, UVW1, UVW2, UVM2)

### Plot Customization
- **X-axis Options**:
  - Modified Julian Date (MJD)
  - Days Since First Observation (DSFO)
  - Days from Peak Magnitude
- **Y-axis Options**:
  - Apparent Magnitude
  - Absolute Magnitude
  - Magnitude Difference from Maximum
- **Plot Types**:
  - Individual Light Curves
  - Color Evolution (e.g., B-V, U-B)
- **Interactive Controls**: Zoom, pan, and export plot data

## 🛠️ Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/aggienova-plots.git
cd aggienova-plots
```

2. Install dependencies
```bash
npm install
```

3. Set up environment variables
```bash
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
```

4. Start the development server
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📊 Usage Examples

### Basic Light Curve Plot
1. Enter a supernova name in the search field
2. Select desired filters using the checkboxes
3. Choose your preferred x-axis and y-axis types
4. The plot will update automatically

### Color Evolution Analysis
1. Switch to "Color" plot type
2. Select two filters for comparison (e.g., B and V for B-V color)
3. The resulting plot shows the color evolution over time

## 🏗️ Technical Stack

- **Frontend**: Next.js, React, TypeScript
- **UI Components**: Material-UI, Tailwind CSS
- **Data Visualization**: Plotly.js
- **Database**: Supabase
- **State Management**: React Context

## 📝 Documentation

Additional documentation is available at the [Wiki](ADD_WIKI_LINK).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dr. Peter Brown
- Aggienova Project Team
- Texas A&M University Department of Physics and Astronomy

---

*Note: This project was made for the Aggienova group at Texas A&M University.*