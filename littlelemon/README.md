# Little Lemon Restaurant API 🍋

A robust and secure Back-End Reservation and Ordering API built using **Django** and **Django REST Framework (DRF)**. This project serves as a comprehensive capstone blueprint that integrates advanced database management (MySQL), token-based authentication, structured role-based access control (RBAC), and API throttling.

---

##  Tech Stack & Tools

- **Backend Framework:** Python 3.x / Django / Django REST Framework (DRF)
- **Database Management:** MySQL (Integrated via DBeaver)
- **Environment Management:** Pipenv
- **Authentication:** Token-based Auth via Djoser
- **API Testing:** Insomnia / Postman

---

##  Core Features

- **User Authentication:** Complete user registration, token generation, and secure login/logout functionalities.
- **Role-Based Access Control (RBAC):** Distinct permissions tailored for **Managers**, **Delivery Crew**, and **Customers**.
- **Cart Management:** Seamless add-to-cart operations with automated cart-clearing mechanics upon successful checkout.
- **Order Dispatch System:** Capabilities for managers to assign pending orders to specific delivery crew members, and for delivery crew to update shipping statuses.
- **Advanced Querying:** Native support for searching, category filtering, and price-range sorting on menu items.
- **API Throttling:** Strict rate-limiting enforced at **5 calls per minute** to safeguard infrastructure from abuse.

---

##  API Endpoints Architecture

### 1. Authentication & User Management (Handled via Djoser)
| Endpoint | Method | Allowed Roles | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/users` | `POST` | Anyone | Registers a new user account |
| `/api/users/me/` | `GET` | Authenticated | Displays current user profile |
| `/token/login/` | `POST` | Anyone | Generates Auth Token upon credentials verify |

### 2. Menu Items & Categories
| Endpoint | Method | Allowed Roles | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/categories` | `GET`, `POST` | Authenticated | Browse or create menu categories |
| `/api/menu-items` | `GET` | Anyone | Lists all items (Supports Search & Filter) |
| `/api/menu-items` | `POST` | Managers Only | Adds a new item to the menu |
| `/api/menu-items/<int:pk>`| `GET` | Anyone | Fetches single menu item details |
| `/api/menu-items/<int:pk>`| `PUT`, `DELETE`| Managers Only | Updates or deletes a menu item |

### 3. Cart Operations
| Endpoint | Method | Allowed Roles | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/cart/menu-items` | `GET` | Customers Only | Views current user's active cart |
| `/api/cart/menu-items` | `POST` | Customers Only | Adds item quantities into the cart |
| `/api/cart/menu-items` | `DELETE`| Customers Only | Empties the user's cart |

### 4. Order Management
| Endpoint | Method | Allowed Roles | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/orders` | `GET` | Authenticated | Customers see own orders; Managers see all |
| `/api/orders` | `POST` | Customers Only | Places an order (Converts Cart to Order) |
| `/api/orders/<int:pk>` | `GET` | Authenticated | Inspects specific order details |
| `/api/orders/<int:pk>` | `PUT`/`PATCH` | Managers / Crew | Managers assign crew; Crew updates status |

### 5. Group & User Roles Management
| Endpoint | Method | Allowed Roles | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/groups/manager/users` | `GET`, `POST`, `DELETE` | Managers Only | Assign or revoke Manager roles |
| `/api/groups/delivery-crew/users`| `GET`, `POST`, `DELETE` | Managers Only | Assign or revoke Delivery Crew roles |

---

##  Installation & Local Setup

Follow these steps to spin up the API server locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/Ehab-ahme/-Capstone-project.git](https://github.com/Ehab-ahme/-Capstone-project.git)
cd your-repo-name
