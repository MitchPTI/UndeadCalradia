def get_object(objects, id):
  for object in objects:
    object_id = object[0]
    if object_id == id:
      return object
  return -1

def get_operations_of_type(operation_list, operation_type):
  list = []
  for i in xrange(0, len(operation_list)):
    operation = operation_list[i]
    if isinstance(operation, (int, long)):
      if operation == operation_type:
        list.append([i, operation])
    else:
      if operation[0] == operation_type:
        list.append([i, operation])
  
  return list

def replace_element(obj_list, old_element, new_element):
  obj_list[obj_list.index(old_element)] = new_element

def replace_sublist(obj_list, old_sublist, new_elements):
  old_sublist_found = 0
  old_sublist_index = 0
  insert_index = 0
  for i in xrange(0, len(obj_list)):
    if obj_list[i] == old_sublist[old_sublist_index]:
      if old_sublist_index == 0:
        insert_index = i
      if old_sublist_index == len(old_sublist) - 1:
        old_sublist_found = 1
        break
      else:
        old_sublist_index = old_sublist_index + 1
    else:
      old_sublist_index = 0
  if old_sublist_found == 1:
    del obj_list[insert_index:insert_index + len(old_sublist) - 1]
    for i in xrange(0, len(new_elements)):
      new_operation = new_elements[i]
      obj_list.insert(insert_index + i, new_operation)
  else:
    print "ERROR: Could not find sublist to replace"
    
def insert_before(obj_list, ref_element, new_elements):
  ref_index = obj_list.index(ref_element)
  for i in xrange(0, len(new_elements)):
    obj_list.insert(ref_index + i, new_elements[i])

def insert_before_op_type(operation_list, ref_operation, new_operations):
  for i in xrange(0, len(operation_list)):
    if operation_list[i][0] == ref_operation:
      for j in xrange(0, len(new_operations)):
        operation_list.insert(i + j, new_operations[j])
  
  for i in xrange(0, len(new_elements)):
    obj_list.insert(ref_index + i, new_elements[i])

def insert_after(obj_list, ref_element, new_elements):
  ref_index = obj_list.index(ref_element) + 1
  for i in xrange(0, len(new_elements)):
    obj_list.insert(ref_index + i, new_elements[i])

def tuple_insert_before(tuple_obj, list_index, ref_element, new_elements):
  tuple_list = list(tuple_obj)
  sublist = tuple_list[list_index]
  ref_index = sublist.index(ref_element)
  for i in xrange(0, len(new_elements)):
    sublist.insert(ref_index + i, new_elements[i])
  
  return tuple(tuple_list)

def tuple_insert_after(tuple_obj, list_index, ref_element, new_elements):
  tuple_list = list(tuple_obj)
  sublist = tuple_list[list_index]
  ref_index = sublist.index(ref_element) + 1
  for i in xrange(0, len(new_elements)):
    sublist.insert(ref_index + i, new_elements[i])
  
  return tuple(tuple_list)