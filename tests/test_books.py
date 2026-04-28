from playwright.sync_api import sync_playwright ,  expect , Page 

# UI Tests-----------------------

# -------------------------------
# Home Page Tests
# -------------------------------
def test_home_page(page: Page):
     page.goto("http://localhost:3000/")
     expect(page).to_have_url("http://localhost:3000/")
     heading = page.get_by_role("heading", name = "Book Library")
     expect(heading).to_have_text("Book Library")

def test_book_count(page : Page):
    page.goto("http://localhost:3000/")
    books= page.locator("a[href$='/book/1']")
    books_count = books.count() 
    expect(books).to_have_count(books_count)
    print("Total no of books:" , books_count)
# -------------------------------
# Book Listing / Navigation------
# -------------------------------
def test_first_book(page : Page):
    page.goto("http://localhost:3000/")
    book= page.locator("a[href$='/book/1']")
    expect(book).to_be_visible
    print("book details:" ,book.inner_text())
    
def test_click_book(page: Page):
    page.goto("http://localhost:3000/")
    book=page.locator("a[href$='/book/1']")
    book.click()
    expect(page).to_have_url("http://localhost:3000/book/1")
    title = page.get_by_role("heading" , name="The Great Gatsby")
    expect(title).to_be_visible

def test_navigation(page: Page):
    page.goto("http://localhost:3000/")
    # Navigate to Book 1
    book1= page.locator("a[href$='/book/1']").click()
    expect(page).to_have_url("http://localhost:3000/book/1")
# Navigate back
    back_button = page.locator("//a[text()='← Back to Library']").click()
    expect(page).to_have_url("http://localhost:3000/")
    # Navigate to Book 2
    book2= page.locator("a[href$='/book/2']").click()
    expect(page).to_have_url("http://localhost:3000/book/2")
    back_button = page.locator("//a[text()='Back to Library']")
    back_button.click()

# -------------------------------
# Book Details Page
# -------------------------------

def test_book_details(page:Page):
    page.goto("http://localhost:3000/")
    book= page.locator("a[href$='/book/1']").click()
    details = page.locator(".p-8")
    # Ensure content is fully loaded
    expect(details).to_be_visible()
    expect(details).not_to_be_empty()
    print("Book Details:", details.inner_text())
    # Validate navigation and add book buttons
    back_button = page.locator("//a[text()='← Back to Library']")
    expect(back_button).to_be_visible()
    Add_book = page.get_by_role("link", name = "Add Another Book")
    expect(Add_book).to_be_visible()

# -------------------------------
# Add Book Flow
# -------------------------------
    
def test_add_book(page:Page):
    page.goto("http://localhost:3000/")
    add_book = page.get_by_role("link", name = "Add New Book")
    expect(add_book).to_be_visible()
    add_book.click()
    expect(page).to_have_url("http://localhost:3000/add-book")
    # Fill form
    title = page.get_by_role("heading" , name="Add New Book")
    expect(title).to_be_visible()
    page.get_by_label("Title *").fill("Test Book")
    page.locator("#author").fill("Test Author")
    page.locator("#genre").select_option("Mystery")
    page.get_by_placeholder("Year").fill("2026")
    page.locator("#pages").fill("100")
    page.get_by_role("textbox", name="ISBN").fill("12345")
    page.get_by_placeholder("Rating out of 5").fill("4")
    page.get_by_placeholder("Enter book description").fill("Test Description")
# Submit form
    Add_Book = page.get_by_role("button" , name = "Add Book")
    expect(Add_Book).to_be_visible()
    Add_Book.click


def test_verify_new_book(page:Page):
    page.goto("http://localhost:3000/")
    book= page.locator("a[href$='/book/6']")
    expect(book).to_be_visible
    print("New Book Found:", book.inner_text())

def test_view_new_book(page:Page):
    page.goto("http://localhost:3000/")
    book=page.locator("a[href$='/book/6']").click()
    expect(page).to_have_url("http://localhost:3000/book/6")
    title = page.get_by_role("heading" , name="Test Book")
    expect(title).to_be_visible
    details =page.locator(".p-8")
    expect(details).to_be_visible()
    print("New Book Details:", details.inner_text())

def test_add_book_cancel(page:Page):
    page.goto("http://localhost:3000/")
    add_book = page.get_by_role("link", name = "Add New Book").click()
    expect(page).to_have_url("http://localhost:3000/add-book")
    cancel_book = page.get_by_role("link", name = "Cancel")
    expect(cancel_book).to_be_visible()
    cancel_book.click()
    expect(page).to_have_url("http://localhost:3000/")

def test_new_book_count(page:Page):
    page.goto("http://localhost:3000/")
    books= page.locator("a[href*='/book']") 
    books_count = books.count() 
    expect(books).to_have_count(books_count) 
    print("Total no of books:" , books_count)

# Negative Scenario
def test_invalid_book(page:Page):
    page.goto("http://localhost:3000/book/100")
    error_message = page.locator("text=Book not found")
    expect(error_message).to_be_visible()


# API Tests----------------------
def test_get_all_books(playwright):
    request = playwright.request.new_context(base_url="http://localhost:3000")
    response = request.get("/api/books")
    assert response.status == 200
    data = response.json()
    print("Total books:", len(data))

def test_get_book_by_id(playwright):
    request = playwright.request.new_context(base_url="http://localhost:3000")
    response = request.get("/api/books/1")
    assert response.status == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "author" in data
    print("Book:", data["title"]) 

# Negative Scenario
def test_get_invalid_book(playwright):
    request = playwright.request.new_context(base_url="http://localhost:3000")
    response = request.get("/api/books/100")
    assert response.status == 404
    print("Invalid book")

def test_create_book(playwright):
    request = playwright.request.new_context(base_url="http://localhost:3000")
    payload = {
        "title": "Test API Book",
        "author": "API Author",
        "genre": "Testing",
        "publishedYear": 1994,
        "description": "Testing API",
        "isbn": "1234",
        "pages": 200,
        "rating": 4.5
    }

    response = request.post("/api/books", data=payload)
    assert response.status == 201 or response.status == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    print("Created book:", data["title"])

# Negative Scenario
def test_create_book_error(playwright):
    request = playwright.request.new_context(base_url="http://localhost:3000")

    payload = {
        "title": ""  
    }

    response = request.post("/api/books", data=payload)
    assert response.status == 400
    print("Validation working correctly")

