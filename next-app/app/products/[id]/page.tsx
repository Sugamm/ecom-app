'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { useCart } from '../../contexts/CartContext'

interface Product {
  id: number
  title: string
  description: string
  price: number
  category: string
  image_url: string
  stock: number
}

export default function ProductDetails() {
  const { id } = useParams()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [quantity, setQuantity] = useState(1)
  const { addToCart } = useCart()

  useEffect(() => {
    fetchProduct()
  }, [id])

  const fetchProduct = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/products/${id}`)
      if (!response.ok) {
        throw new Error('Failed to fetch product')
      }
      const data = await response.json()
      setProduct(data)
    } catch (err) {
      setError('An error occurred while fetching the product')
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = async () => {
    if (product) {
      try {
        await addToCart({ ...product, product_id: product.id, quantity })
        alert('Product added to cart')
      } catch (err) {
        alert('Failed to add product to cart')
      }
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>{error}</div>
  if (!product) return <div>Product not found</div>

  return (
    <div className="flex flex-col md:flex-row">
      <div className="md:w-1/2">
        <img src={product.image_url} alt={product.title} className="w-full h-auto" />
      </div>
      <div className="md:w-1/2 md:pl-8">
        <h1 className="text-3xl font-bold mb-4">{product.title}</h1>
        <p className="text-gray-600 mb-4">{product.category}</p>
        <p className="text-xl font-bold mb-4">${product.price.toFixed(2)}</p>
        <p className="mb-4">{product.description}</p>
        <p className="mb-4">In stock: {product.stock}</p>
        <div className="flex items-center mb-4">
          <label htmlFor="quantity" className="mr-2">
            Quantity:
          </label>
          <input
            type="number"
            id="quantity"
            min="1"
            max={product.stock}
            value={quantity}
            onChange={(e) => setQuantity(Math.min(Math.max(1, parseInt(e.target.value)), product.stock))}
            className="border p-2 w-16"
          />
        </div>
        <button
          onClick={handleAddToCart}
          disabled={product.stock === 0}
          className={`px-4 py-2 ${
            product.stock === 0
              ? 'bg-gray-300 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
        >
          {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      </div>
    </div>
  )
}

