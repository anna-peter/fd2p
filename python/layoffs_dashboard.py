import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Use a theme from bootswatch.com
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

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

def get_state_layoffs(top_n):
    return master_df.groupby('State')['Layoffs'].sum().nlargest(top_n).reset_index()

def get_company_layoffs(top_n):
    return master_df.groupby('Company')['Layoffs'].sum().nlargest(top_n).reset_index()

def get_monthly_layoffs():
    if 'WARN Received Date' not in master_df.columns:
        return pd.DataFrame(columns=['Month name', 'Number of Workers', 'Month Num'])
    df = master_df.copy()
    df['Month'] = pd.to_datetime(df['WARN Received Date'], errors='coerce').dt.month
    df['Month name'] = pd.to_datetime(df['WARN Received Date'], errors='coerce').dt.strftime('%B')
    monthly_total = df.groupby('Month name', sort=False)['Layoffs'].sum().reset_index()
    monthly_total['Month Num'] = pd.to_datetime(monthly_total['Month name'], format='%B').dt.month
    monthly_total = monthly_total.sort_values('Month Num')
    monthly_total = monthly_total.rename(columns={'Layoffs': 'Number of Workers'})
    return monthly_total

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Tech Layoffs in 2025', className='text-center my-4'), width=12)
    ], className="mb-4"),

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
                dbc.Tab(
                    dcc.Graph(
                        id='state-treemap',
                        figure=px.treemap(
                            get_state_layoffs(20),  # Provide default top_n value
                            path=['State'],
                            values='Layoffs',
                            title='Tech Layoffs by State (2025): CA, NY, TX, WA',
                            color='Layoffs',
                            color_continuous_scale=px.colors.sequential.Blues
                        )
                    ), label='By State', tab_id='tab-state', className='p-4'),
                dbc.Tab(
                    dcc.Graph(
                        id='company-treemap',
                        figure=px.treemap(
                            get_company_layoffs(20),  # Provide default top_n value
                            path=['Company'],
                            values='Layoffs',
                            title='Tech Layoffs by Company (2025)',
                            color='Layoffs',
                            color_continuous_scale=px.colors.sequential.Greens
                        )
                    ), label='By Company', tab_id='tab-company', className='p-4'),
                dbc.Tab(
                    dcc.Graph(
                        id='month-treemap',
                        figure=px.treemap(
                            get_monthly_layoffs(),
                            path=['Month name'],
                            values='Number of Workers',
                            title='Total Layoffs by Month in Major Tech Companies',
                            color='Number of Workers',
                            color_continuous_scale=px.colors.sequential.Greens
                        )
                    ), label='By Month', tab_id='tab-month', className='p-4'),
                dbc.Tab(
                    html.Div([
                        html.H4("Startup Job Postings"),
                        html.Video(
                            controls=True,
                            src="/assets/YCjobs.mp4",
                            style={"width": "100%", "maxWidth": "720px"}
                        )
                    ]), label='Jobs', tab_id='tab-video', className='p-4'),
            ], id='tabs', active_tab='tab-state', className='mb-4'),
        ], className="p-0") # Remove padding from card body to let graph fill space
    ]),
], fluid=True, className="dbc") # The "dbc" class helps with theme integration


@app.callback(
    Output('state-treemap', 'figure'),
    Output('company-treemap', 'figure'),
    Output('month-treemap', 'figure'),
    Input('tabs', 'active_tab'),
    Input('top-n-slider', 'value')
)
def update_treemaps(active_tab, top_n):
    state_layoffs = get_state_layoffs(top_n)
    company_layoffs = get_company_layoffs(top_n)
    monthly_layoffs = get_monthly_layoffs()

    fig_state = px.treemap(
        state_layoffs, path=['State'], values='Layoffs',
        color='Layoffs', color_continuous_scale=px.colors.sequential.Mint
    )
    fig_company = px.treemap(
        company_layoffs, path=['Company'], values='Layoffs',
        color='Layoffs', color_continuous_scale=px.colors.sequential.PuBu
    )
    fig_month = px.treemap(
        monthly_layoffs, path=['Month name'], values='Number of Workers',
        color='Number of Workers', color_continuous_scale=px.colors.sequential.Greens
    )

    for fig in [fig_state, fig_company, fig_month]:
        fig.update_layout(
            title=None,
            margin=dict(t=10, l=10, r=10, b=10),
            font=dict(family="sans-serif"),
        )
        fig.update_traces(
            textinfo='label+value',
            texttemplate='%{label}<br>%{value:,.0f}',
            hovertemplate='<b>%{label}</b><br>Total Layoffs: %{value:,.0f}<extra></extra>'
        )

    if active_tab == 'tab-state':
        return fig_state, dash.no_update, dash.no_update
    elif active_tab == 'tab-company':
        return dash.no_update, fig_company, dash.no_update
    elif active_tab == 'tab-month':
        return dash.no_update, dash.no_update, fig_month
    return fig_state, fig_company, fig_month

if __name__ == '__main__':
    app.run(debug=True)