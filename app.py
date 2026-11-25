
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Gene Expression Data Explorer",
    page_icon="🧬",
    layout="wide"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}
h1 {
    color: #17365D;
}
h2, h3 {
    color: #286090;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("🧬 Gene Expression Data Explorer")
st.markdown(
    "### An Interactive Computational Biology Analysis Platform"
)
st.write(
    "Upload gene expression datasets, explore numerical "
    "patterns and generate statistical visualizations."
)

st.divider()

# SIDEBAR
st.sidebar.title("🧬 Navigation")
st.sidebar.info("Computational Biology Project")
st.sidebar.write("Gene Expression Analysis")
st.sidebar.write("Python | Streamlit | Pandas")

# DATA UPLOAD
st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your gene expression CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        data = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        # OVERVIEW
        st.header("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Samples / Rows", data.shape[0])
        col2.metric("Total Variables", data.shape[1])
        col3.metric(
            "Missing Values",
            int(data.isnull().sum().sum())
        )

        # DATA PREVIEW
        st.header("🔬 Dataset Preview")
        st.dataframe(data, use_container_width=True)

        # NUMERIC ANALYSIS
        numeric_data = data.select_dtypes(
            include="number"
        )

        if not numeric_data.empty:

            st.header("📈 Gene Expression Analysis")

            gene = st.selectbox(
                "Select a numerical gene / variable",
                numeric_data.columns
            )

            values = numeric_data[gene].dropna()

            # EXPRESSION PROFILE
            st.subheader("Expression Profile")

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.plot(
                values.values,
                marker="o",
                linewidth=2
            )

            ax.set_title(f"Expression Profile: {gene}")
            ax.set_xlabel("Sample Index")
            ax.set_ylabel("Expression Level")
            ax.grid(alpha=0.3)

            st.pyplot(fig)
            plt.close(fig)

            # DISTRIBUTION
            st.subheader("Expression Distribution")

            fig2, ax2 = plt.subplots(figsize=(10, 4))

            ax2.hist(values, bins=20)
            ax2.set_title(f"Distribution of {gene}")
            ax2.set_xlabel("Expression Level")
            ax2.set_ylabel("Frequency")
            ax2.grid(alpha=0.2)

            st.pyplot(fig2)
            plt.close(fig2)

            # STATISTICS
            st.subheader("📋 Statistical Analysis")

            stats = values.describe()

            st.dataframe(
                stats.to_frame(name="Statistics"),
                use_container_width=True
            )

            # CORRELATION
            st.subheader("Correlation Matrix")

            if numeric_data.shape[1] >= 2:

                corr = numeric_data.corr()

                fig3, ax3 = plt.subplots(figsize=(9, 6))

                image = ax3.imshow(
                    corr,
                    cmap="coolwarm",
                    aspect="auto",
                    vmin=-1,
                    vmax=1
                )

                ax3.set_xticks(range(len(corr.columns)))
                ax3.set_yticks(range(len(corr.columns)))

                ax3.set_xticklabels(
                    corr.columns,
                    rotation=45,
                    ha="right"
                )

                ax3.set_yticklabels(corr.columns)

                fig3.colorbar(image, ax=ax3)

                st.pyplot(fig3)
                plt.close(fig3)

            # DOWNLOAD
            st.subheader("⬇️ Export Results")

            st.download_button(
                label="Download Dataset as CSV",
                data=data.to_csv(index=False),
                file_name="gene_expression_results.csv",
                mime="text/csv"
            )

        else:
            st.warning(
                "No numerical columns found in this dataset."
            )

    except Exception as error:
        st.error(f"Dataset error: {error}")

else:

    st.info(
        "Upload a CSV dataset above to begin your analysis."
    )

    st.header("✨ Platform Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📂 Data Upload")
        st.write("Upload and preview CSV datasets.")

    with col2:
        st.subheader("📈 Visualization")
        st.write("Explore expression profiles and distributions.")

    with col3:
        st.subheader("📊 Statistics")
        st.write("Calculate descriptive statistics and correlations.")

    st.header("🔍 Analysis Workflow")

    st.write("""
    1. Upload a gene expression dataset.
    2. Explore the dataset structure.
    3. Select a numerical variable.
    4. Generate expression visualizations.
    5. Examine statistical summaries and correlations.
    6. Download the dataset.
    """)

st.divider()

st.caption(
    "Gene Expression Data Explorer | Computational Biology Project"
)
