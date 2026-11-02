import csv


def loadinventory():
    invent = []
    try:
        with open("inventory.csv","r",newline="") as fobj:
            for record in csv.reader(fobj):
                if record:
                    invent.append({
                        "code":record[0],
                        "name":record[1],
                        "price":float(record[2]),
                        "quantity":int(record[3])
                    })
    except FileNotFoundError:
        pass
    return invent


def storeinventory(invent):
    with open("inventory.csv","w",newline="") as fobj:
        writer = csv.writer(fobj)
        for item in invent:
            writer.writerow([
                item["code"],item["name"],
                item["price"],item["quantity"]
            ])


def loadbillnos():
    billnos = []
    try:
        with open("bills.csv","r",newline="") as fobj:
            for record in csv.reader(fobj):
                if record:
                    billnos.append(int(record[0]))
    except FileNotFoundError:
        pass
    return billnos


def storecustomerbills(bills):
    with open("bills.csv","a",newline="") as fobj:
        writer = csv.writer(fobj)
        writer.writerows(bills)


class InvalidPriceError(Exception):
    pass


class InvalidStockError(Exception):
    pass


class InvalidInputCombinationError(Exception):
    pass


class DuplicateBillError(Exception):
    pass


def main():
    try:
        invent = loadinventory()
        billnos = loadbillnos()
    except (OSError,ValueError,IndexError) as e:
        print("Cannot load files:",e)
        return

    while(True):
        print("\n1 - Add item to inventory")
        print("2 - Purchase Items")
        print("3 - Exit")

        try:
            choice = int(input("Enter your choice : "))

            if (choice == 3):
                return

            elif (choice == 1):
                pid = input("Enter the product id : ")
                productname = input("Enter the product name : ")
                price = float(input("Enter the price : "))
                stock = int(input("Enter the stock : "))

                if (price <= 0):
                    raise InvalidPriceError("Price must be above 0")
                if (stock < 0):
                    raise InvalidStockError("Stock must be at least 0")

                flag = True
                for item in invent:
                    if (item["code"] == pid):
                        if (item["name"] != productname):
                            raise InvalidInputCombinationError(
                                "For matching code, product names must match"
                            )
                        item["price"] = price
                        item["quantity"] = stock
                        print("Edited existing item")
                        flag = False
                        break

                if flag:
                    invent.append({
                        "code":pid,"name":productname,
                        "price":price,"quantity":stock
                    })
                    print("Item added")

                storeinventory(invent)

            elif (choice == 2):
                bno = int(input("Enter the bill id : "))
                if (bno <= 0):
                    raise ValueError("Bill number must be positive")
                if bno in billnos:
                    raise DuplicateBillError("Bill number already exists")

                name = input("Customer name : ")
                n = int(input("Number of purchase entries : "))
                if (n <= 0):
                    raise ValueError("Enter at least one item")

                purchased_items = []
                total = 0

                for i in range(n):
                    pid = input("Product id : ")
                    qty = int(input("Quantity : "))

                    if (qty <= 0):
                        raise InvalidStockError("Quantity must be positive")

                    product = None
                    for item in invent:
                        if (item["code"] == pid):
                            product = item
                            break

                    if product is None:
                        raise ValueError("Invalid product code")

                    # Include earlier entries of this product in the same bill.
                    required = qty
                    for code,quantity in purchased_items:
                        if (code == pid):
                            required += quantity

                    if (required > product["quantity"]):
                        raise InvalidStockError("Insufficient stock")

                    purchased_items.append((pid,qty))
                    total += qty * product["price"]

                # Reduce stock only after all purchase entries are valid.
                for code,quantity in purchased_items:
                    for item in invent:
                        if (item["code"] == code):
                            item["quantity"] -= quantity
                            break

                bill = (bno,name,tuple(purchased_items),round(total,2))

                storeinventory(invent)
                storecustomerbills([bill])
                billnos.append(bno)

                print("\nBill number :",bno)
                print("Customer :",name)
                print("Items :",purchased_items)
                print("Total :",round(total,2))

            else:
                print("Invalid choice")

        except (InvalidPriceError,InvalidStockError,
                InvalidInputCombinationError,DuplicateBillError) as e:
            print(e)
        except ValueError as e:
            print("Invalid input:",e)
        except OSError as e:
            print("File error:",e)


if __name__ == '__main__':
    main()
