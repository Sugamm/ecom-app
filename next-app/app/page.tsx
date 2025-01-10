'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useCart } from './contexts/CartContext'

interface Product {
  id: number
  title: string
  price: number
  category: string
  image_url: string
  stock: number
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const { addToCart } = useCart()

  useEffect(() => {
    fetchProducts()
  }, [page, search, category])

  const fetchProducts = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/products?page=${page}&search=${search}&category=${category}`)
      if (!response.ok) {
        throw new Error('Failed to fetch products')
      }
      const data = await response.json()
      setProducts(data.products)
      setTotalPages(data.pages)
    } catch (err) {
      setError('An error occurred while fetching products')
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = async (product: Product) => {
    try {
      await addToCart({ ...product, product_id: product.id, quantity: 1 })
      alert('Product added to cart')
    } catch (err) {
      alert('Failed to add product to cart')
    }
  }

  if (loading) return <div className="text-center py-10">Loading...</div>
  if (error) return <div className="text-center py-10 text-red-500">{error}</div>

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Our Products</h1>
      <div className="mb-8 flex flex-col sm:flex-row gap-4">
      <form onSubmit={(e) => e.preventDefault()} className="relative flex-grow">
          <input
            type="text"
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10 w-full"
          />
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
        </form>
        <div className="relative">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="input appearance-none pr-10"
          >
            <option value="">All Categories</option>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Books">Books</option>
            <option value="Home & Garden">Home & Garden</option>
            <option value="Toys">Toys</option>
          </select>
          <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </span>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <div key={product.id} className="card">
            <Link href={`/products/${product.id}`}>
              <img src={product.image_url} alt={product.title} className="w-full h-48 object-cover" />
            </Link>
            <div className="p-4">
              <Link href={`/products/${product.id}`}>
                <h2 className="text-xl font-semibold mb-2 hover:text-blue-600">{product.title}</h2>
              </Link>
              <p className="text-gray-600 mb-2">{product.category}</p>
              <p className="text-2xl font-bold mb-4">${product.price.toFixed(2)}</p>
              <button
                onClick={() => handleAddToCart(product)}
                disabled={product.stock === 0}
                className={`btn w-full ${
                  product.stock === 0
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'btn-primary'
                }`}
              >
                {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
              </button>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-8 flex justify-center">
        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
          className="btn btn-secondary mr-2"
        >
          Previous
        </button>
        <span className="px-4 py-2 bg-white rounded">
          Page {page} of {totalPages}
        </span>
        <button
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
          className="btn btn-secondary ml-2"
        >
          Next
        </button>
      </div>
    </div>
  )
}

