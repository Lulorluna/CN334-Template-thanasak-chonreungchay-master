import { useEffect, useState } from 'react';

export default function SummaryPage() {
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        const fetchSummary = async () => {
            try {
                const [userRes, productRes] = await Promise.all([
                    fetch("http://127.0.0.1:3342/api/summarize"),
                    fetch("http://127.0.0.1:3341/api/summarize/")
                ]);
                const userData = await userRes.json();
                const productData = await productRes.json();

                setSummary({
                    user_count: userData.count,
                    ...productData
                });
            } catch (err) {
                console.error("Error fetching summary:", err);
            }
        };

        fetchSummary();
    }, []);

    if (!summary) return <p>Loading...</p>;

    return (
        <main className="bg-black text-white min-h-screen p-10">
            <h1 className="text-3xl mb-4">System Summary</h1>
            <p>Users: {summary.user_count}</p>
            <p>Products: {summary.product_count}</p>
            <p>Orders: {summary.order_count}</p>
            <p>Total Items Sold: {summary.total_quantity_sold}</p>
        </main>
    );
}
