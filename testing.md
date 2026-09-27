# Testing Documentation

## Testing Approach

The Student Academic Performance System was tested by running the application and checking the major operations through the menu-driven interface.

## Test Cases

| Test Case | Operation | Expected Result | Status |
|---|---|---|---|
| TC01 | Start application | Main menu is displayed | Pass |
| TC02 | Add new student | Student record is stored successfully | Pass |
| TC03 | Add duplicate registration number | System reports that registration number already exists | Pass |
| TC04 | Search student | Matching student record is displayed | Pass |
| TC05 | View all students | Stored student records are displayed | Pass |
| TC06 | Invalid menu choice | System handles invalid input appropriately | Pass |
| TC07 | Database operation | Student data is stored/retrieved from SQLite | Pass |
| TC08 | Program exit | Application exits normally | Pass |

## Validation

The application was manually tested using different inputs, including valid and duplicate student registration numbers. The duplicate registration number validation was successfully observed during testing.

## Result

The major tested functions of the application operated as expected during manual testing.