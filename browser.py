import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QLabel, QTabWidget, QToolBar)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont

class VeloxBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Velox Browser")
        self.showMaximized()
        self.setStyleSheet("background-color: #000000; color: white;") 

        # --- Tabs ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # --- Toolbar ---
        toolbar = QToolBar()
        toolbar.setStyleSheet("background: #000; border: none; padding: 5px;")
        self.addToolBar(toolbar)
        
        undo_btn = QPushButton("⬅️")
        undo_btn.clicked.connect(lambda: self.tabs.currentWidget().findChild(QWebEngineView).back())
        toolbar.addWidget(undo_btn)
        
        redo_btn = QPushButton("➡️")
        redo_btn.clicked.connect(lambda: self.tabs.currentWidget().findChild(QWebEngineView).forward())
        toolbar.addWidget(redo_btn)

        # --- + Add Tab Button ---
        add_btn = QPushButton("+")
        add_btn.setStyleSheet("padding: 0 15px; font-size: 18px;")
        add_btn.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(add_btn, Qt.Corner.TopRightCorner)

        self.add_new_tab()

    def close_tab(self, i):
        if self.tabs.count() <= 1:
            self.close()
        else:
            self.tabs.removeTab(i)

    def add_new_tab(self):
        browser = QWebEngineView()
        browser.loadFinished.connect(self.apply_velox_theme)
        
        # --- Home Screen ---
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("VELOX")
        title.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        title.setStyleSheet("color: #3498db; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        url_bar = QLineEdit()
        url_bar.setStyleSheet("padding: 15px; border-radius: 25px; background: #111; color: white; border: 1px solid #444;")
        
        search_btn = QPushButton("Search 🔍")
        search_btn.setStyleSheet("padding: 15px 25px; background: #3498db; color: white; border-radius: 25px;")
        search_btn.clicked.connect(lambda: self.load_url(url_bar.text(), browser, home_widget))
        
        layout.addWidget(url_bar)
        layout.addWidget(search_btn)

        container = QWidget()
        cont_layout = QVBoxLayout(container)
        cont_layout.setContentsMargins(0,0,0,0)
        cont_layout.addWidget(home_widget)
        cont_layout.addWidget(browser)
        browser.hide()

        self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentWidget(container)

    def load_url(self, text, browser, home_widget):
        if not text: return
        browser.setUrl(QUrl(f"https://www.bing.com/search?q={text}"))
        home_widget.hide()
        browser.show()

    def apply_velox_theme(self):
        js = """
        var style = document.createElement('style');
        style.innerHTML = `
            #id_h, #id_l, .b_logHeader, .b_rewards, #b_header, .b_sbox, .b_sw_hdr, footer {
                display: none !important;
            }
            .velox-branding { font-size: 30px; color: #3498db; padding: 10px; border-bottom: 2px solid #3498db; }
        `;
        document.head.appendChild(style);
        document.body.insertAdjacentHTML('afterbegin', '<div class="velox-branding">VELOX</div>');
        """
        browser = self.tabs.currentWidget().findChild(QWebEngineView)
        if browser:
            browser.page().runJavaScript(js)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VeloxBrowser()
    window.show()
    sys.exit(app.exec())