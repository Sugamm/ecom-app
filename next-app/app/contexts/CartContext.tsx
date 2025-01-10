'use client'

import { createContext, useContext, useState, useEffect } from 'react'
import { useAuth } from './AuthContext'

interface CartItem {
  id: number
  product_id: number
  title: string
  price: number
  quantity: number
  stock: number
}

interface CartContextType {
  cartItems: CartItem[]
  addToCart: (product: CartItem) => Promise<void>
  updateCartItem: (id: number, quantity: number) => Promise<void>
  removeFromCart: (id: number) => Promise<void>
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cartItems, setCartItems] = useState<CartItem[]>([])
  const { user } = useAuth()

  useEffect(() => {
    if (user) {
      fetchCart()
    } else {
      setCartItems([])
    }
  }, [user])

  const fetchCart = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/cart', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      setCartItems(data)
    }
  }

  const addToCart = async (product: CartItem) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ product_id: product.product_id, quantity: product.quantity })
      });
  
      if (response.ok) {
        await fetchCart();
      } else if (response.status === 422) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Invalid data sent to the server');
      } else {
        throw new Error('Failed to add item to cart');
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      throw error;
    }
  }

  const updateCartItem = async (id: number, quantity: number) => {
    const response = await fetch('http://127.0.0.1:5000/api/cart/update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ cart_item_id: id, quantity })
    })
    if (response.ok) {
      await fetchCart()
    } else {
      throw new Error('Failed to update cart item')
    }
  }

  const removeFromCart = async (id: number) => {
    const response = await fetch('http://127.0.0.1:5000/api/cart/remove', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ cart_item_id: id })
    })
    if (response.ok) {
      await fetchCart()
    } else {
      throw new Error('Failed to remove item from cart')
    }
  }

  return (
    <CartContext.Provider value={{ cartItems, addToCart, updateCartItem, removeFromCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

