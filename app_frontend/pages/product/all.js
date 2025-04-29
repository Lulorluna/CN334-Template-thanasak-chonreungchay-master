import { useState, useEffect } from 'react';

export default function ProductList() {
    const [products, setProducts] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('jwt_access');
        if (!token) {
            setError("Not authenticated. Please log in.");
            return;
        }

        fetch('http://127.0.0.1:3341/api/product/all/', {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then(res => {
                if (res.status === 401) throw new Error("Unauthorized. Please log in.");
                if (!res.ok) throw new Error("Failed to fetch products.");
                return res.json();
            })
            .then(data => setProducts(data.data))
            .catch(err => setError(err.message));
    }, []);

    if (error) return <p>{error}</p>;
    if (!products) return <p>Loading products...</p>;

    return (
        <main className="flex min-h-screen flex-col items-center justify-between">
            <div style={{ fontSize: "64px" }}
                className="w-full flex flex-col justify-center items-center">
                <div>All Products</div>
                <div>
                    {products.map(product => (
                        <div key={product.id} className="mb-6">
                            <p><strong>Name:</strong> {product.name}</p>
                            <p><strong>Description:</strong> {product.description}</p>
                            <p><strong>Price:</strong> ${product.price}</p>
                            <p><strong>Stock:</strong> {product.stock}</p>
                        </div>
                    ))}
                </div>
            </div>
        </main>
    );
}
