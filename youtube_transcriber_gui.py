#!/usr/bin/env python3
"""
YouTube Transcriber - Desktop GUI Application
A modern, user-friendly desktop application for extracting YouTube transcripts.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import os
from datetime import datetime
from youtube_transcriber import YouTubeTranscriber, URLExtractor

class YouTubeTranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Transcriber")
        self.root.geometry("900x700")
        
        # Initialize transcriber
        self.transcriber = YouTubeTranscriber()
        self.url_extractor = URLExtractor()
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Configure the visual style of the application"""
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Big.TButton', font=('Arial', 10), padding=10)
    
    def create_widgets(self):
        """Create all GUI elements"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Transcriber", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # URL Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(0, weight=1)
        
        # URL Entry
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, font=('Arial', 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.bind('<Return>', lambda e: self.process_video())
        
        # Process Button
        self.process_btn = ttk.Button(input_frame, text="Get Transcript", 
                                     command=self.process_video, style='Big.TButton')
        self.process_btn.grid(row=0, column=1)
        
        # Example URLs
        example_label = ttk.Label(input_frame, 
                                 text="Supports: youtube.com/watch?v=..., youtu.be/..., shorts, live URLs, or just video ID",
                                 font=('Arial', 9), foreground='gray')
        example_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Options Section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Include Metadata Checkbox
        self.include_metadata = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(options_frame, text="Include video metadata (title, duration, uploader)",
                                        variable=self.include_metadata)
        metadata_check.grid(row=0, column=0, sticky=tk.W)
        
        # Status Section
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=0, pady=5)
        
        # Video Info Section (initially hidden)
        self.info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="10")
        self.info_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.grid_remove()  # Hide initially
        
        # Video info labels
        self.title_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.uploader_var = tk.StringVar()
        
        ttk.Label(self.info_frame, text="Title:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(self.info_frame, textvariable=self.title_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.info_frame, text="Duration:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(self.info_frame, textvariable=self.duration_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(self.info_frame, text="Uploader:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(self.info_frame, textvariable=self.uploader_var).grid(row=2, column=1, sticky=tk.W)
        
        # Transcript Section
        transcript_frame = ttk.LabelFrame(main_frame, text="Transcript", padding="10")
        transcript_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        transcript_frame.columnconfigure(0, weight=1)
        transcript_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Transcript Text Area
        self.transcript_text = scrolledtext.ScrolledText(transcript_frame, wrap=tk.WORD, 
                                                        font=('Arial', 10), height=15)
        self.transcript_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button Frame
        button_frame = ttk.Frame(transcript_frame)
        button_frame.grid(row=1, column=0, pady=(10, 0))
        
        # Save and Copy Buttons
        self.save_btn = ttk.Button(button_frame, text="Save to File", 
                                   command=self.save_transcript, state='disabled')
        self.save_btn.grid(row=0, column=0, padx=5)
        
        self.copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", 
                                   command=self.copy_transcript, state='disabled')
        self.copy_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", 
                                    command=self.clear_all)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Batch Processing Button
        self.batch_btn = ttk.Button(button_frame, text="Batch Process", 
                                   command=self.open_batch_dialog)
        self.batch_btn.grid(row=0, column=3, padx=5)
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def process_video(self):
        """Process the video URL in a separate thread"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Input Required", "Please enter a YouTube URL or video ID")
            return
        
        # Disable controls during processing
        self.process_btn.config(state='disabled')
        self.url_entry.config(state='disabled')
        self.status_var.set("Processing...")
        self.status_label.config(style='')
        
        # Clear previous content
        self.transcript_text.delete(1.0, tk.END)
        self.info_frame.grid_remove()
        
        # Process in thread to avoid freezing GUI
        thread = threading.Thread(target=self._process_video_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _process_video_thread(self, url):
        """Process video in background thread"""
        try:
            # Extract video ID
            video_id = self.url_extractor.extract_video_id(url)
            if not video_id:
                self.root.after(0, self._show_error, "Invalid YouTube URL or video ID")
                return
            
            # Update status
            self.root.after(0, lambda: self.status_var.set(f"Extracting transcript for video ID: {video_id}"))
            
            # Get metadata if requested
            metadata = {}
            if self.include_metadata.get():
                metadata = self.transcriber.get_video_metadata(video_id)
                
                # Update video info in GUI
                self.root.after(0, self._update_video_info, metadata)
            
            # Extract transcript
            transcript = self.transcriber.extract_transcript(video_id)
            
            if transcript:
                # Success - update GUI
                self.root.after(0, self._show_transcript, transcript, metadata)
            else:
                self.root.after(0, self._show_error, "No transcript available for this video")
                
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_video_info(self, metadata):
        """Update video information in GUI"""
        self.title_var.set(metadata.get('title', 'Unknown'))
        
        duration = metadata.get('duration', 0)
        if duration:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            if hours > 0:
                self.duration_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            else:
                self.duration_var.set(f"{minutes:02d}:{seconds:02d}")
        else:
            self.duration_var.set("Unknown")
        
        self.uploader_var.set(metadata.get('uploader', 'Unknown'))
        self.info_frame.grid()
    
    def _show_transcript(self, transcript, metadata):
        """Display transcript in GUI"""
        # Insert transcript
        self.transcript_text.insert(1.0, transcript)
        
        # Update status
        self.status_var.set("Transcript extracted successfully!")
        self.status_label.config(style='Success.TLabel')
        
        # Enable buttons
        self.save_btn.config(state='normal')
        self.copy_btn.config(state='normal')
        self.process_btn.config(state='normal')
        self.url_entry.config(state='normal')
        
        # Store for saving
        self.current_transcript = transcript
        self.current_metadata = metadata
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.status_var.set(f"Error: {error_msg[:100]}")
        self.status_label.config(style='Error.TLabel')
        self.process_btn.config(state='normal')
        self.url_entry.config(state='normal')
        
        # Show full error in messagebox if it's long
        if len(error_msg) > 100:
            messagebox.showerror("Error", error_msg)
    
    def save_transcript(self):
        """Save transcript to file"""
        if not hasattr(self, 'current_transcript'):
            return
        
        # Generate default filename
        title = self.current_metadata.get('title', 'transcript')
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:100]  # Limit length
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"{safe_title}_{timestamp}.txt"
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if file_path:
            try:
                # Prepare content
                content = []
                if self.include_metadata.get() and self.current_metadata:
                    content.append("=" * 80)
                    content.append(f"Title: {self.current_metadata.get('title', 'Unknown')}")
                    content.append(f"Uploader: {self.current_metadata.get('uploader', 'Unknown')}")
                    content.append(f"Duration: {self.duration_var.get()}")
                    content.append("=" * 80)
                    content.append("")
                
                content.append(self.current_transcript)
                
                # Save to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(content))
                
                messagebox.showinfo("Success", f"Transcript saved to:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")
    
    def copy_transcript(self):
        """Copy transcript to clipboard"""
        if hasattr(self, 'current_transcript'):
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_transcript)
            self.status_var.set("Transcript copied to clipboard!")
            self.status_label.config(style='Success.TLabel')
    
    def clear_all(self):
        """Clear all fields"""
        self.url_var.set("")
        self.transcript_text.delete(1.0, tk.END)
        self.info_frame.grid_remove()
        self.status_var.set("Ready")
        self.status_label.config(style='')
        self.save_btn.config(state='disabled')
        self.copy_btn.config(state='disabled')
    
    def open_batch_dialog(self):
        """Open batch processing dialog"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Processing")
        batch_window.geometry("600x400")
        
        # Instructions
        ttk.Label(batch_window, text="Enter YouTube URLs (one per line):", 
                 font=('Arial', 11)).pack(pady=10)
        
        # URL text area
        url_text = scrolledtext.ScrolledText(batch_window, height=15, width=70)
        url_text.pack(padx=10, pady=5)
        
        # Output directory frame
        dir_frame = ttk.Frame(batch_window)
        dir_frame.pack(pady=10)
        
        ttk.Label(dir_frame, text="Output Directory:").grid(row=0, column=0, padx=5)
        dir_var = tk.StringVar(value=os.getcwd())
        dir_entry = ttk.Entry(dir_frame, textvariable=dir_var, width=40)
        dir_entry.grid(row=0, column=1, padx=5)
        
        def browse_dir():
            directory = filedialog.askdirectory()
            if directory:
                dir_var.set(directory)
        
        ttk.Button(dir_frame, text="Browse", command=browse_dir).grid(row=0, column=2)
        
        # Process button
        def process_batch():
            urls = url_text.get(1.0, tk.END).strip().split('\n')
            urls = [url.strip() for url in urls if url.strip() and not url.startswith('#')]
            
            if not urls:
                messagebox.showwarning("No URLs", "Please enter at least one URL")
                return
            
            output_dir = dir_var.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            batch_window.destroy()
            
            # Process in main window
            self.status_var.set(f"Processing {len(urls)} videos...")
            messagebox.showinfo("Batch Processing", 
                              f"Processing {len(urls)} videos.\nFiles will be saved to:\n{output_dir}")
            
            # Run batch processing in thread
            thread = threading.Thread(target=self._batch_process_thread, 
                                    args=(urls, output_dir))
            thread.daemon = True
            thread.start()
        
        ttk.Button(batch_window, text="Process All", 
                  command=process_batch).pack(pady=10)
    
    def _batch_process_thread(self, urls, output_dir):
        """Process multiple URLs in background"""
        results = self.transcriber.process_batch(urls, output_dir, 
                                                self.include_metadata.get(), 
                                                quiet=True)
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        msg = f"Batch processing complete!\n\nProcessed: {len(results)} videos\nSuccessful: {successful}\nFailed: {failed}"
        
        if failed > 0:
            msg += "\n\nFailed URLs:\n"
            for url, success in results.items():
                if not success:
                    msg += f"- {url}\n"
        
        self.root.after(0, lambda: messagebox.showinfo("Batch Complete", msg))
        self.root.after(0, lambda: self.status_var.set("Ready"))


def main():
    """Main entry point for GUI application"""
    root = tk.Tk()
    app = YouTubeTranscriberGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()