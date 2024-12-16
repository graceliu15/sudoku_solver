from django import forms

class SudokuForm(forms.Form):
    # Create 81 input fields for the 9x9 grid
    grid = [
        [forms.CharField(max_length=1, required=False) for _ in range(9)]
        for _ in range(9)
    ]

    # This will allow you to access each row easily
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add the fields to the form
        for i in range(9):
            for j in range(9):
                self.fields[f'cell_{i}_{j}'] = forms.CharField(required=False, 
                        widget=forms.TextInput(attrs={
                        'class': 'grid-cell',
                        # 'size': '1',  # Make input very small
                        # 'maxlength': '1',
                        'style': 'width:100px; text-align:center;'
                    }))
        # field1 = forms.CharField(max_length=100)
        # field2 = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        board = []

        # Convert cleaned data into a 2D list (9x9 grid)
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = cleaned_data.get(f'cell_{i}_{j}')
                row.append(int(cell_value) if cell_value != "" else -1)  # Use None for empty cells
            board.append(row)

        return board
