import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function OrderByProductIdPage() {
    const router = useRouter();
    const { id } = router.query;

    const [orders, setOrders] = useState([]);
    const [product, setProduct] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!id) return;

        const fetchData = async () => {
            const token = localStorage.getItem('jwt_access');
            const response = await fetch(`http://127.0.0.1:3341/api/order/byProductId/${id}/`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (response.ok) {
                setProduct(data.product);
                setOrders(data.orders);
                setError(null);
            } else {
                setProduct(null);
                setOrders([]);
                setError(data.error);
            }
        };

        fetchData();
    }, [id]);

    if (!product && !error) return <p className="text-white bg-black min-h-screen flex items-center justify-center">Loading...</p>;

    return (
        <main className="flex min-h-screen flex-col items-center justify-start bg-black text-white p-6">
            <div style={{ fontSize: "64px", marginBottom: "20px" }}>
                Orders for Product ID: {id}
            </div>
            {error && <p>{error}</p>}

            {product && (
                <div style={{ marginBottom: "20px" }}>
                    <div>Name: {product.name}</div>
                    <div>Category: {product.category}</div>
                    <div>Price: {product.price}</div>
                </div>
            )}

            {orders.length === 0 && !error ? (
                <p>No orders found for this product.</p>
            ) : (
                <ul>
                    {orders.map((orderItem, index) => (
                        <li key={index}>
                            Order #{orderItem.order} | Quantity: {orderItem.quantity} | Unit Price: {orderItem.unit_price} |
                            Total Price: {orderItem.total_price}
                        </li>
                    ))}
                </ul>
            )}
        </main>
    );
}
