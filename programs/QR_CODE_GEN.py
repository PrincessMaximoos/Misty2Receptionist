import qrcode

def generate_qr_code(data, output_filename):
    """
    Generate a QR code from the given data and save it as an image file.
    
    :param data: The data to encode in the QR code
    :param output_filename: The filename for the output QR code image
    """
    try:
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')
        
        # Save the image
        img.save(output_filename)
        
        print(f"QR code successfully saved as {output_filename}")
    except Exception as e:
        print(f"Error generating QR code: {e}")

# Example usage
if __name__ == "__main__":
    # data = input("Please enter what you wish to turn into a qr code:")
    # data = "Name: Benhur Bastaki, Company: Staffs Uni, Visitor: 2"
    # data = "Name: Max McGill, Company: Staffs Uni, Visitor: 1"
    data = "quit"
    generate_qr_code(data, "qr_codes/qrcode.png")