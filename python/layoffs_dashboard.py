import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Use a theme from bootswatch.com
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# --- 1. EFFICIENT DATA LOADING ---
# Load and combine all data into a single DataFrame at startup.
def load_all_data():
    state_files = {
        'California': '../data/tech_layoffs_ca_cleaned.csv',
        'New York': '../data/tech_layoffs_ny_cleaned.csv',
        'Texas': '../data/tech_layoffs_tx_cleaned.csv',
        'Washington': '../data/tech_layoffs_wa_cleaned.csv',
    }
    all_data = []
    for state, path in state_files.items():
        try:
            df = pd.read_csv(path)
            # Standardize column names if they differ
            df = df.rename(columns={'Number of Workers': 'Layoffs'})
            if 'Layoffs' not in df.columns:
                continue # Skip files without layoff numbers
            
            df['State'] = state # Add a 'State' column
            all_data.append(df[['Company', 'Layoffs', 'State']])
        except Exception as e:
            print(f"Could not load or process {path}: {e}")
            
    if not all_data:
        # Return an empty DataFrame with the expected columns if no data is loaded
        return pd.DataFrame(columns=['Company', 'Layoffs', 'State'])
        
    master_df = pd.concat(all_data, ignore_index=True)
    master_df['Layoffs'] = pd.to_numeric(master_df['Layoffs'], errors='coerce').fillna(0).astype(int)
    master_df['Company'] = master_df['Company'].str.strip().str.title()
    return master_df

# Load the data once
master_df = load_all_data()

# --- 2. PRE-CALCULATE KPIs ---
total_layoffs = master_df['Layoffs'].sum()
num_companies = master_df['Company'].nunique()

# kpi_layoffs_card = dbc.Card(dbc.CardBody([
#     html.H6("Total Layoffs", className="card-title text-muted"),
#     html.P(f"{total_layoffs:,.0f}", className="card-text fs-2 fw-bold")
# ]), className="text-center p-3")

# kpi_companies_card = dbc.Card(dbc.CardBody([
#     html.H6("Companies Affected", className="card-title text-muted"),
#     html.P(f"{num_companies}", className="card-text fs-2 fw-bold")
# ]), className="text-center p-3")

# --- 3. REBUILT APP LAYOUT ---
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Tech Layoffs in 2025', className='text-center my-4'), width=12)
    ]),

    # dbc.Row([
    #     dbc.Col(kpi_layoffs_card, md=4),
    #     dbc.Col(kpi_companies_card, md=4),
    # ], justify="center", className="mb-4"),

    dbc.Card([
        dbc.CardHeader(
            html.Div([
                html.Label("Number of Companies/States to Display:", className="fw-bold me-2"),
                dcc.Slider(
                    id='top-n-slider', min=5, max=50, step=5, value=20,
                    marks={i: str(i) for i in range(5, 51, 5)},
                )
            ], className="d-flex align-items-center")
        ),
        dbc.CardBody([
            dbc.Tabs([
                dbc.Tab(dcc.Graph(id='state-treemap', style={'height': '60vh'}), label='By State', tab_id='tab-state'),
                dbc.Tab(dcc.Graph(id='company-treemap', style={'height': '60vh'}), label='By Company', tab_id='tab-company'),
            ], id='tabs', active_tab='tab-state')
        ], className="p-0") # Remove padding from card body to let graph fill space
    ]),
], fluid=True, className="dbc") # The "dbc" class helps with theme integration


# --- 4. DYNAMIC CALLBACK ---
@app.callback(
    Output('state-treemap', 'figure'),
    Output('company-treemap', 'figure'),
    Input('tabs', 'active_tab'),
    Input('top-n-slider', 'value')
)
def update_treemaps(active_tab, top_n):
    # Group and filter data based on slider
    state_layoffs = master_df.groupby('State')['Layoffs'].sum().nlargest(top_n).reset_index()
    company_layoffs = master_df.groupby('Company')['Layoffs'].sum().nlargest(top_n).reset_index()

    # Create base figures
    fig_state = px.treemap(
        state_layoffs, path=['State'], values='Layoffs',
        color='Layoffs', color_continuous_scale=px.colors.sequential.Mint
    )
    fig_company = px.treemap(
        company_layoffs, path=['Company'], values='Layoffs',
        color='Layoffs', color_continuous_scale=px.colors.sequential.PuBu
    )

    # Apply consistent styling to both figures
    for fig in [fig_state, fig_company]:
        fig.update_layout(
            title=None,
            margin=dict(t=10, l=10, r=10, b=10),
            font=dict(family="sans-serif"),
        )
        # *** THIS IS THE CORRECTED AND SAFE VERSION ***
        fig.update_traces(
            textinfo='label+value',
            texttemplate='%{label}<br>%{value:,.0f}',
            hovertemplate='<b>%{label}</b><br>Total Layoffs: %{value:,.0f}<extra></extra>'
            # The 'depthfade' property has been removed to ensure compatibility
        )
    
    # Efficiently update only the visible tab
    if active_tab == 'tab-state':
        return fig_state, dash.no_update
    elif active_tab == 'tab-company':
        return dash.no_update, fig_company

    return fig_state, fig_company

if __name__ == '__main__':
    app.run(debug=True)