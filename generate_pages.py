import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract head, header, footer
head_match = re.search(r'(<!DOCTYPE html>.*?<body[^>]*>)', index_html, re.DOTALL)
header_match = re.search(r'(<!-- Floating Action Buttons -->.*?</header>)', index_html, re.DOTALL)
footer_match = re.search(r'(<!-- Footer -->.*?</html>)', index_html, re.DOTALL)

if not (head_match and header_match and footer_match):
    print("Could not find sections in index.html")
    exit(1)

head = head_match.group(1)
header = header_match.group(1)
footer = footer_match.group(1)

# Update footer links in the footer template
footer = footer.replace('href="#"', 'href="{}"')

def create_page(filename, title, content_html):
    page_head = head.replace('<title>Hotel Rajdhani | Premium Stay in Thiruvananthapuram</title>', f'<title>{title} | Hotel Rajdhani</title>')
    page_content = f"""
    <main class="flex-grow pt-32 pb-20 px-4 md:px-6">
        <div class="max-w-4xl mx-auto">
            <div class="text-center mb-12">
                <span class="text-gold-600 font-bold text-xs uppercase tracking-[0.2em] block mb-2">Legal Information</span>
                <h1 class="text-4xl md:text-5xl text-royal-900 font-bold mb-4">{title}</h1>
                <div class="h-1 w-20 bg-gold-600 mx-auto rounded-full"></div>
            </div>
            <div class="bg-white p-8 md:p-12 rounded-3xl shadow-xl shadow-gray-100 border border-gray-100 relative overflow-hidden">
                <div class="relative z-10 space-y-8">
                    {content_html}
                    <div class="text-center pt-8 border-t border-gray-100">
                        <a href="index.html" class="inline-flex items-center gap-2 text-royal-500 hover:text-blue-600 font-bold uppercase tracking-widest text-xs transition-colors">
                            <i class="fas fa-arrow-left"></i> Back to Homepage
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>
"""
    # Fix the footer formatting string to use proper link replacements
    page_footer = re.sub(r'<a href="\{\}" class="hover:text-gold-500 transition-colors">Privacy Policy</a>', '<a href="privacy-policy.html" class="hover:text-gold-500 transition-colors">Privacy Policy</a>', footer)
    page_footer = re.sub(r'<a href="\{\}" class="hover:text-gold-500 transition-colors">Terms & Conditions</a>', '<a href="terms-and-conditions.html" class="hover:text-gold-500 transition-colors">Terms & Conditions</a>', page_footer)
    page_footer = re.sub(r'<a href="\{\}" class="hover:text-gold-500 transition-colors">Cancellation Policy</a>', '<a href="disclaimer.html" class="hover:text-gold-500 transition-colors">Disclaimer</a>', page_footer)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_head + '\n' + header + '\n' + page_content + '\n' + page_footer)

# Privacy Policy Content
privacy_content = """
                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-file-contract text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Cancellation / Prepayment</h3>
                            <p class="text-royal-500 leading-relaxed font-light">
                                Cancellation and prepayment policies vary according to room type. Please check the specific conditions when selecting your accommodation. We appreciate your understanding.
                            </p>
                        </div>
                    </div>

                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-user-check text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Age Requirement</h3>
                            <p class="text-royal-500 leading-relaxed font-light">
                                The primary guest must be at least <strong>18 years of age</strong> to check into Hotel Rajdhani. Minors must be accompanied by guardians.
                            </p>
                        </div>
                    </div>

                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-id-card text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Identification Requirements</h3>
                            <p class="text-royal-500 leading-relaxed mb-4 font-light">
                                As per Government regulations, it is mandatory for all guests to carry a <strong>valid photo identity card and address proof</strong> at the time of check-in (Aadhar Card, Driving License, Voter ID, or Passport).
                            </p>
                            <div class="bg-red-50 p-4 rounded-xl border-l-4 border-red-500">
                                <p class="text-red-800 text-sm font-medium flex items-center gap-2">
                                    <i class="fas fa-exclamation-circle"></i> Note: If check-in is denied due to lack of required documents, the booking may be treated as cancelled.
                                </p>
                            </div>
                        </div>
                    </div>
"""

# Terms & Conditions Content
terms_content = """
                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-id-card-clip text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Check-in & Identification</h3>
                            <div class="text-royal-500 leading-relaxed font-light">
                                <p class="mb-3">
                                    As per Government regulations, all guests (including minors) must present a <strong>valid Photo ID</strong> (Aadhar/Passport/Voter ID) upon check-in. PAN Cards are not accepted as valid address proof.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-ban text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Hotel Rules</h3>
                            <p class="text-royal-500 leading-relaxed mb-4 font-light">
                                To ensure a comfortable stay for all our guests, we request you to follow the hotel rules. Please respect the property and other guests.
                            </p>
                            <ul class="list-disc pl-5 space-y-2 text-royal-500 mb-4 font-light">
                                <li>No smoking in non-smoking rooms.</li>
                                <li>Damage to hotel property will be charged to the guest.</li>
                                <li>Outside visitors are not allowed in rooms after 10:00 PM.</li>
                            </ul>
                        </div>
                    </div>
"""

# Disclaimer Content
disclaimer_content = """
                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-info-circle text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">General Information</h3>
                            <p class="text-royal-500 leading-relaxed font-light">
                                All information provided on the <strong>Hotel Rajdhani</strong> website is for general information purposes only. We aim to provide an accurate representation of our rooms and services.
                            </p>
                        </div>
                    </div>

                    <div class="flex gap-6 items-start pb-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 text-blue-600">
                            <i class="fas fa-sync-alt text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-royal-900 mb-3">Accuracy & Updates</h3>
                            <p class="text-royal-500 leading-relaxed font-light">
                                While we strive for accuracy regarding room availability and facilities, details and pricing are subject to change without notice. We request guests to verify details at the time of booking.
                            </p>
                        </div>
                    </div>
"""

create_page('privacy-policy.html', 'Privacy Policy', privacy_content)
create_page('terms-and-conditions.html', 'Terms & Conditions', terms_content)
create_page('disclaimer.html', 'Disclaimer', disclaimer_content)

print("Pages created successfully")
