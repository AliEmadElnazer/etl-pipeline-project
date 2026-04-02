
    def load_currency_rates(self):
        """Load or create currency exchange rates lookup table"""
        # TODO: Replace with actual API call or database lookup
        currency_rates = {
            'USD': 1.0,
            'CAD': 0.74,
            'EUR': 1.09,
            'GBP': 1.27,
            'AUD': 0.67
        }
        return currency_rates

    def convert_currency(self, df, source_currency='USD', target_currency='USD'):
        """Convert prices using exchange rates"""
        if "price" not in df.columns:
            return df

        rates = self.load_currency_rates()
        
        if source_currency in rates and target_currency in rates:
            conversion_rate = rates[target_currency] / rates[source_currency]
            df['price_original'] = df['price']
            df['price_converted'] = df['price'] * conversion_rate
            df['currency_source'] = source_currency
            df['currency_target'] = target_currency
            df['exchange_rate_applied'] = conversion_rate

        return df

    def calculate_delivery_metrics(self, df):
        """Add delivery performance metrics"""
        if "order_date" not in df.columns or "delivery_date" not in df.columns:
            return df

        # Convert to datetime
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')

        # Calculate latency in days
        df['delivery_latency_days'] = (df['delivery_date'] - df['order_date']).dt.days

        # Expected delivery (e.g., 5 business days)
        expected_delivery_days = 5
        df['is_late_delivery'] = df['delivery_latency_days'] > expected_delivery_days

        # Delivery performance score (0-100)
        df['delivery_performance_score'] = np.where(
            df['is_late_delivery'],
            np.maximum(0, 100 - (df['delivery_latency_days'] - expected_delivery_days) * 10),
            100
        )

        return df

    def add_locality_flag(self, df, store_locations=None):
        """Determine if customer is local based on proximity to stores"""
        if "zip_code" not in df.columns:
            return df

        # Default store locations (zip codes)
        if store_locations is None:
            store_locations = ['10002', '11550', '75126', '95008', '90274']

        df['is_local_customer'] = df['zip_code'].astype(str).isin(store_locations)
        df['locality_flag'] = df['is_local_customer'].map({True: 'LOCAL', False: 'NON_LOCAL'})

        return df

    def create_order_status_lookup(self):
        """Create lookup table for order statuses"""
        status_lookup = {
            'ORD_NEW': 1,
            'ORD_PENDING': 2,
            'ORD_PROCESSING': 3,
            'ORD_SHIPPED': 4,
            'ORD_DELIVERED': 5,
            'ORD_CANCELLED': 6,
            'ORD_RETURNED': 7
        }
        return status_lookup

    def resolve_order_status(self, df):
        """Resolve ambiguous status columns using lookup table"""
        if "status" not in df.columns:
            return df

        status_lookup = self.create_order_status_lookup()
        df['status_code'] = df['status'].map(status_lookup)
        df['status_name'] = df['status']

        return df

    def process_stage_2(self, df):
        """Apply all Stage 2 transformations"""
        # Currency conversion
        df = self.convert_currency(df, source_currency='USD', target_currency='USD')

        # Delivery metrics
        df = self.calculate_delivery_metrics(df)

        # Locality flag
        df = self.add_locality_flag(df)

        # Order status resolution
        df = self.resolve_order_status(df)

        # Add transformation metadata
        df['transformed_at'] = datetime.now().isoformat()
        df['data_quality_stage'] = 'STAGING_2'

        return df

    def save_stage_2(self, df, file_name):
        """Save transformed data to Stage 2"""
        os.makedirs(self.staging_2_path, exist_ok=True)
        output_path = os.path.join(self.staging_2_path, file_name)
        df.to_csv(output_path, index=False)
        print(f"✓ Saved to Stage 2: {output_path}")

    # ============ Main Pipeline ============

    def run(self):
        """Run complete ETL pipeline: Stage 1 + Stage 2"""
        print("🧹 Running Data Quality Pipeline...")
        print("=" * 50)

        files = os.listdir(self.input_path)

        for file in files:
            if file.endswith(".csv"):
                print(f"\n📄 Processing: {file}")

                # Stage 1: Cleaning
                print("  → Stage 1: Data Cleaning...")
                df_stage_1 = self.process_stage_1(file)
                print(f"    ✓ Rows after cleaning: {len(df_stage_1)}")

                # Stage 2: Transformation
                print("  → Stage 2: Data Transformation...")
                df_stage_2 = self.process_stage_2(df_stage_1)
                self.save_stage_2(df_stage_2, file)
                print(f"    ✓ Rows after transformation: {len(df_stage_2)}")

        print("\n" + "=" * 50)
        print("✅ Data Quality Pipeline Complete!")
