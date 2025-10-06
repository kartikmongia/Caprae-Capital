import pandas as pd
if domain.endswith(('.com', '.io', '.ai', '.co')) and len(domain.split('.'))>=2:
return 3
return 2




def dedupe_df(df):
# normalize company + email
df['company_norm'] = df['company'].fillna("").apply(normalize_company)
df['email_norm'] = df['email'].fillna("").str.strip().str.lower()
df['phone_norm'] = df['phone'].fillna("").str.replace(r"\D", "", regex=True)
# keep first occurrence of (company_norm + email_norm) or (company_norm + phone_norm)
df['dup_key'] = df.apply(lambda r: (r['company_norm'] + '|' + (r['email_norm'] or r['phone_norm'])), axis=1)
before = len(df)
df = df.drop_duplicates(subset=['dup_key'])
df = df.drop(columns=['dup_key'])
after = len(df)
return df, before-after




if uploaded_file:
df = pd.read_csv(uploaded_file)
# normalize expected columns
for c in ['company','email','phone','country']:
if c not in df.columns:
df[c] = ""
st.write("Preview:")
st.dataframe(df.head())


# enrichment
with st.spinner('Enriching...'):
df['inferred_domain'] = df['company'].apply(infer_domain_from_company)
df['email_score'] = df['email'].apply(email_score)


removed = 0
df, removed = dedupe_df(df)


st.success(f"Enrichment done. {removed} duplicates removed.")


st.markdown("### Filters")
min_score = st.slider('Minimum email score', 0, 3, 2)
country_filter = st.text_input('Country (leave blank for all)')


filtered = df[df['email_score'] >= min_score]
if country_filter:
filtered = filtered[filtered['country'].str.contains(country_filter, case=False, na=False)]


st.write(f"{len(filtered)} leads after filtering")
st.dataframe(filtered.head(50))


csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button('Download CSV', data=csv, file_name='enriched_leads.csv', mime='text/csv')


st.markdown("---")
st.markdown("#### Notes & next steps:\n- This demo uses heuristics for domain inference and email scoring; in production, integrate 3rd-party enrichment APIs (Clearbit, Hunter, Snov.io) for higher fidelity.\n- Add async scraping + rate-limiting and proxy rotation for scale.\n- Add unit tests and CI pipeline before shipping.")
